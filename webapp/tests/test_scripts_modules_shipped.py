"""Guard: every scripts/ module webapp/ imports at MODULE SCOPE is actually
COPYed into the Docker image. Sibling of test_skill_files_shipped.py, same
failure shape, different asset class (Python modules instead of skill folders).

The failure this prevents is not silent, it is total. webapp/services/
submissions.py did `from scripts.evals import fetch_submission_corpora as
extraction` at module scope; webapp/routers/case_studies.py imports
submissions at module scope; webapp/main.py imports that router at module
scope. The Dockerfile copied the other scripts/evals files but not that one.
On Railway that import chain runs the instant uvicorn imports the app, so the
container never bound a port -- not a degraded case-study feature, the WHOLE
APP (candidate queue, drafting, values scorecards, everything) went down with
it. The repo checkout on disk still has the file, so no local "does it import"
smoke test caught it; only a static check of the Dockerfile itself can.

Scope is deliberately MODULE-LEVEL, TOP-OF-FILE imports only -- the exact
shape of the bug above. A deferred import inside a function body, especially
one already guarded by its own try/except (e.g. submissions.py's own
`_log_gmail_read` importing scripts.utils.audit_log, which swallows any
ImportError so a missing audit logger degrades logging, not the app), cannot
take uvicorn down at startup the way an unconditional top-level import can,
and is a different, much smaller-blast-radius class of bug this guard does
not claim to cover.
"""

from __future__ import annotations

import ast
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WEBAPP_DIR = os.path.join(ROOT, "webapp")


def _read(rel: str) -> str:
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def _all_webapp_py_files() -> list[str]:
    files = []
    for dirpath, dirnames, filenames in os.walk(WEBAPP_DIR):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in filenames:
            if fn.endswith(".py"):
                files.append(os.path.join(dirpath, fn))
    return sorted(files)


def _module_level_scripts_import_candidates(py_path: str) -> list[str]:
    """Every dotted `scripts....` path a module-scope import statement in
    py_path COULD be resolving to. `from scripts.evals import foo` might mean
    "the submodule scripts/evals/foo.py" or "the attribute foo of
    scripts/evals/__init__.py" -- both dotted forms are yielded and resolved
    against the filesystem by the caller, which is the only way to tell which
    one is real without executing the import."""
    with open(py_path, encoding="utf-8") as fh:
        source = fh.read()
    tree = ast.parse(source, filename=py_path)

    candidates: list[str] = []
    for node in tree.body:  # module (top) level only -- see module docstring
        if isinstance(node, ast.ImportFrom):
            if node.level != 0 or not node.module:
                continue  # relative import; never scripts.*
            if node.module.split(".")[0] != "scripts":
                continue
            for alias in node.names:
                candidates.append(f"{node.module}.{alias.name}")
            candidates.append(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] == "scripts":
                    candidates.append(alias.name)
    return candidates


def _resolve_to_shipped_file(dotted: str) -> str | None:
    """dotted -> the scripts/.../thing.py path on disk it names, or None if
    dotted does not correspond to an actual file (e.g. it names an attribute
    inside a module, not a module itself)."""
    rel = dotted.replace(".", "/") + ".py"
    return rel if os.path.isfile(os.path.join(ROOT, rel)) else None


def test_every_module_scope_scripts_import_has_a_matching_dockerfile_copy():
    dockerfile = _read("Dockerfile")
    missing: set[tuple[str, str]] = set()

    for py_path in _all_webapp_py_files():
        rel_py = os.path.relpath(py_path, ROOT).replace(os.sep, "/")
        for dotted in _module_level_scripts_import_candidates(py_path):
            resolved = _resolve_to_shipped_file(dotted)
            if resolved is None:
                continue
            copy_line = f"COPY {resolved} {resolved}"
            if copy_line not in dockerfile:
                missing.add((rel_py, resolved))

    assert not missing, (
        "webapp/ imports these scripts/ modules at module scope with no "
        "matching 'COPY <path> <path>' line in the Dockerfile -- deploying "
        "would raise ModuleNotFoundError during app import and take the "
        f"whole app down: {sorted(missing)}"
    )
