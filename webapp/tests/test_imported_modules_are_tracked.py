"""Every module the app imports must be committed to git.

THE OUTAGE THIS EXISTS FOR (2026-09-25). Commit e1894bb changed
`webapp/main.py` to import `webapp.routers.tech_screening` and pushed, but
`webapp/routers/tech_screening.py` itself was never `git add`ed. Railway builds
from the commit, so the image contained a `main.py` importing a file that was
not in it. Every boot died with

    ImportError: cannot import name 'tech_screening' from 'webapp.routers'

and the whole app returned 502, not just the new page. Ten modules were
untracked at that moment, across two features.

WHY NOTHING CAUGHT IT. Locally the file is on disk, so every import works,
every test passes, and `python -m webapp.main` runs. The defect is invisible
from inside the working tree and only appears once the tree is reconstructed
from git. That is the same shape as the fake-session SQL bug: a check that
never leaves the developer's machine cannot see what the deployment will see.

HOW THIS WORKS. Import the app, then walk `sys.modules` for everything under
`webapp` and assert each file appears in `git ls-files`. Untracked means it
will not be in the image.

⚠️ THIS TEST IS SUPPOSED TO FAIL WHILE YOU ARE WRITING A NEW MODULE, from the
   moment you wire it into `main.py` until you commit it. That is the whole
   point, and the fix is `git add`, never a skip.

⚠️ LIMIT: `git ls-files` reads the INDEX, so a file that is staged but not yet
   committed counts as tracked. That is the right trade for day-to-day work,
   and it still catches the real case, where the file was neither staged nor
   committed. It does not catch staging a file and then committing without it.

Run: python -m pytest webapp/tests/test_imported_modules_are_tracked.py -v
"""

from __future__ import annotations

import pathlib
import subprocess
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[2]


def _tracked_files() -> set[str]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=REPO, capture_output=True, text=True, timeout=60
    )
    if out.returncode != 0:
        pytest.skip(f"git unavailable: {out.stderr[:200]}")
    return {line.strip() for line in out.stdout.splitlines() if line.strip()}


def _imported_app_modules() -> list[str]:
    """Repo-relative paths of every `webapp.*` module the app pulls in.

    `webapp.main` is imported here rather than at module scope so the walk
    sees exactly what a real boot loads, including routers reached only
    through `include_router`.
    """
    import webapp.main  # noqa: F401  (the import IS the subject of the test)

    paths = []
    for name, module in list(sys.modules.items()):
        if not name.startswith("webapp"):
            continue
        filename = getattr(module, "__file__", None)
        if not filename:
            continue
        try:
            rel = pathlib.Path(filename).resolve().relative_to(REPO).as_posix()
        except ValueError:
            continue  # installed elsewhere; not ours to ship
        paths.append(rel)
    return sorted(set(paths))


def test_the_walk_finds_the_app():
    """A collector that silently finds nothing would make the real test below
    pass while checking no modules at all."""
    found = _imported_app_modules()
    assert "webapp/main.py" in found
    assert len(found) > 20, found


def test_every_imported_webapp_module_is_tracked_by_git():
    tracked = _tracked_files()
    untracked = [p for p in _imported_app_modules() if p not in tracked]
    assert not untracked, (
        "These modules are imported by the app but are NOT committed, so they "
        "will be missing from the deployed image and every boot will die with "
        "ImportError:\n  " + "\n  ".join(untracked) + "\n\n"
        "Run `git add` on each of them. Do not skip this test: this is exactly "
        "how production went down on 2026-09-25."
    )


def test_the_check_would_have_caught_the_outage():
    """Proof it bites. A tracked-set that is missing a real module must be
    reported, or a bug in the comparison would make the test above vacuous."""
    tracked = _tracked_files() - {"webapp/routers/tech_screening.py"}
    untracked = [p for p in _imported_app_modules() if p not in tracked]
    assert "webapp/routers/tech_screening.py" in untracked


def test_alembic_migrations_are_tracked():
    """Same failure mode, different directory. A model referencing a table
    whose migration was never committed fails at request time rather than at
    boot, which is slower to diagnose and just as broken."""
    tracked = _tracked_files()
    on_disk = {
        p.relative_to(REPO).as_posix()
        for p in (REPO / "alembic" / "versions").glob("*.py")
    }
    untracked = sorted(on_disk - tracked)
    assert not untracked, (
        "Migrations on disk but not committed:\n  " + "\n  ".join(untracked)
    )


# --------------------------------------------------------------------------
# The same failure, on the frontend side
# --------------------------------------------------------------------------

# e1894bb's own message records that App.tsx had already imported a page that
# was not in the tree, so this has happened in both directions. A missing .tsx
# breaks the Vite build instead of the Python boot, which fails the deploy
# rather than crash-looping it, but it is the same mistake and the same fix.

_FRONTEND = REPO / "frontend" / "src"
_REL_IMPORT = __import__("re").compile(
    r"""(?:^|\n)\s*(?:import|export)[^'"\n]*?from\s+['"](\.[^'"]+)['"]""",
)


def _resolve(importer: pathlib.Path, spec: str) -> pathlib.Path | None:
    """The file a relative TS import actually names, trying each extension."""
    base = (importer.parent / spec).resolve()
    for candidate in (
        base, base.with_suffix(".ts"), base.with_suffix(".tsx"),
        base / "index.ts", base / "index.tsx",
    ):
        if candidate.is_file():
            return candidate
    return None


def test_every_frontend_module_imported_by_a_page_is_tracked():
    if not _FRONTEND.is_dir():
        pytest.skip("no frontend/src in this checkout")
    tracked = _tracked_files()
    sources = sorted(
        p for ext in ("*.ts", "*.tsx") for p in _FRONTEND.rglob(ext)
    )
    assert sources, "found no frontend sources to check"

    untracked: set[str] = set()
    for source in sources:
        try:
            body = source.read_text(encoding="utf-8")
        except OSError:
            continue
        for spec in _REL_IMPORT.findall(body):
            target = _resolve(source, spec)
            if target is None:
                continue  # unresolvable here (alias, type-only); tsc's job
            rel = target.relative_to(REPO).as_posix()
            if rel not in tracked:
                untracked.add(rel)

    assert not untracked, (
        "These frontend modules are imported but NOT committed, so the Vite "
        "build in the image will fail on a missing file:\n  "
        + "\n  ".join(sorted(untracked))
    )


def _resolved_frontend_imports() -> set[str]:
    out: set[str] = set()
    for source in (p for ext in ("*.ts", "*.tsx") for p in _FRONTEND.rglob(ext)):
        try:
            body = source.read_text(encoding="utf-8")
        except OSError:
            continue
        for spec in _REL_IMPORT.findall(body):
            target = _resolve(source, spec)
            if target is not None:
                out.add(target.relative_to(REPO).as_posix())
    return out


def test_the_frontend_scan_actually_resolves_imports():
    """A regex that matched nothing would make the check above pass on an
    empty set, which is the failure mode that makes a guard worthless."""
    if not _FRONTEND.is_dir():
        pytest.skip("no frontend/src in this checkout")
    resolved = _resolved_frontend_imports()
    assert len(resolved) > 25, len(resolved)
    # App.tsx imports every page, so the pages must be in there.
    assert any(p.startswith("frontend/src/pages/") for p in resolved)


def test_the_frontend_check_bites():
    """Proof, by removing a real page from the tracked set."""
    if not _FRONTEND.is_dir():
        pytest.skip("no frontend/src in this checkout")
    page = "frontend/src/pages/InvitesPage.tsx"
    resolved = _resolved_frontend_imports()
    assert page in resolved, "the page this test relies on is no longer imported"
    tracked = _tracked_files() - {page}
    assert page in sorted(r for r in resolved if r not in tracked)
