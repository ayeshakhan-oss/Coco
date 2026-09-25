"""CV Screening and Technical Screening are two skills and must never merge.

Run: python -m pytest webapp/tests/test_screening_skills_stay_separate.py -v

🔒 NON-NEGOTIABLE (Ayesha, 2026-09-25). The two stay separate until she says
otherwise, in those words. They look similar from a distance and share a data
source, which is exactly why a drifting edit would not be noticed: both read
Markaz applications, both score a CV against a JD, both end in tiers. What
makes them different is the thing that matters.

    CV Screening        coco.cv_screens, Coco's three criteria, tiers
                        shortlist / maybe / no_hire, thresholds calibrated
                        against people Taleemabad actually hired.

    Technical Screening public.nugget_screening_*, Nugget's weighted rubric
                        with hard filters, tiers P1-P4 / MANUAL_REVIEW /
                        UNUSABLE, thresholds P1>=85 P2>=70.

A score from one means nothing in the other's vocabulary. Merging them, or
letting one quietly read the other's tables or tier names, would produce a
number that looks comparable and is not.

WHAT THIS ENFORCES, and deliberately nothing more:

  1. Neither side imports the other.
  2. Neither side names the other's tables in executable code.
  3. Neither side uses the other's tier vocabulary in executable code.
  4. The two routers keep distinct URL prefixes.
  5. The two frontend pages do not import each other.

Comments are exempt on purpose. Both modules carry header comments explaining
the separation and naming the other side's tables to do it, which is the
behaviour we want, so every check below reads the AST (imports and string
literals) rather than raw text. A comment cannot execute.

Per CLAUDE.md Rule 25, a gate that has only ever passed proves nothing, so
the second half of this file feeds the checkers deliberately broken source and
asserts each one fires.
"""

from __future__ import annotations

import ast
import os
import re

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- the two sides ----------------------------------------------------------

CV_MODULES = (
    "webapp/services/cv_screening.py",
    "webapp/routers/cv_screening.py",
)

TECH_MODULES = (
    "webapp/routers/tech_screening.py",
    "webapp/routers/evaluations.py",
    "webapp/services/nugget_reads.py",
    "webapp/services/nugget_writes.py",
    "webapp/services/screening_runs.py",
    "webapp/services/tech_tiering.py",
    "webapp/services/rubric_drafting.py",
)

# Module name fragments each side must not import from the other.
CV_ONLY_IMPORTS = ("cv_screening",)
TECH_ONLY_IMPORTS = (
    "tech_screening",
    "nugget_reads",
    "nugget_writes",
    "screening_runs",
    "tech_tiering",
    "rubric_drafting",
)

# Table names, matched inside string literals (where SQL lives).
CV_TABLES = re.compile(r"coco\.cv_screens|coco\.cv_screen_skips|cv_screen_skips", re.I)
TECH_TABLES = re.compile(r"nugget_screening_", re.I)

# Tier vocabulary, matched inside string literals.
CV_TIERS = re.compile(r"\b(shortlist|no_hire)\b")
TECH_TIERS = re.compile(r"\b(P[1-4]|MANUAL_REVIEW|UNUSABLE)\b")


def _read(rel: str) -> str:
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def _existing(rels: tuple[str, ...]) -> list[str]:
    """Only check modules that are actually on disk.

    Tech screening is mid-build; a module that does not exist yet must not fail
    the suite, but the moment it appears it is covered.
    """
    return [r for r in rels if os.path.isfile(os.path.join(ROOT, r))]


# --- the checkers, which the broken-source tests below also use -------------


def imported_names(source: str) -> set[str]:
    """Every module path this source imports. Comments cannot appear here."""
    names: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            names.add(base)
            for alias in node.names:
                names.add(f"{base}.{alias.name}" if base else alias.name)
    return names


def string_literals(source: str) -> list[str]:
    """Every string constant in the source. Comments are not constants."""
    return [
        node.value
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    ]


def executable_strings(source: str) -> list[str]:
    """String constants minus docstrings.

    A module, class or function docstring is documentation that happens to be
    a string constant. Both sides explain the separation in their docstrings
    and name the other's tables while doing it, which is correct.
    """
    tree = ast.parse(source)
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = ast.get_docstring(node, clean=False)
            if doc is not None:
                docstrings.add(doc)
    return [s for s in string_literals(source) if s not in docstrings]


def forbidden_imports(source: str, forbidden: tuple[str, ...]) -> list[str]:
    return sorted(
        {name for name in imported_names(source) if any(f in name for f in forbidden)}
    )


def forbidden_matches(source: str, pattern: re.Pattern[str]) -> list[str]:
    hits: list[str] = []
    for literal in executable_strings(source):
        hits.extend(pattern.findall(literal))
    return sorted({h if isinstance(h, str) else h[0] for h in hits})


# --- 1 and 2: the real modules on disk --------------------------------------


@pytest.mark.parametrize("rel", _existing(CV_MODULES))
def test_cv_screening_does_not_import_technical_screening(rel):
    offenders = forbidden_imports(_read(rel), TECH_ONLY_IMPORTS)
    assert not offenders, (
        f"{rel} imports technical screening: {offenders}. "
        "These are two separate skills and must not be merged (Ayesha, non-negotiable)."
    )


@pytest.mark.parametrize("rel", _existing(TECH_MODULES))
def test_technical_screening_does_not_import_cv_screening(rel):
    offenders = forbidden_imports(_read(rel), CV_ONLY_IMPORTS)
    assert not offenders, (
        f"{rel} imports CV screening: {offenders}. "
        "These are two separate skills and must not be merged (Ayesha, non-negotiable)."
    )


@pytest.mark.parametrize("rel", _existing(CV_MODULES))
def test_cv_screening_does_not_query_nugget_tables(rel):
    offenders = forbidden_matches(_read(rel), TECH_TABLES)
    assert not offenders, (
        f"{rel} names Nugget's tables in executable code: {offenders}. "
        "CV screening owns coco.cv_screens and reads nothing of Nugget's."
    )


@pytest.mark.parametrize("rel", _existing(TECH_MODULES))
def test_technical_screening_does_not_query_cv_screen_tables(rel):
    offenders = forbidden_matches(_read(rel), CV_TABLES)
    assert not offenders, (
        f"{rel} names CV screening's tables in executable code: {offenders}. "
        "Technical screening owns public.nugget_screening_* and reads nothing of Coco's CV screen."
    )


# --- 3: tier vocabulary -----------------------------------------------------


@pytest.mark.parametrize("rel", _existing(CV_MODULES))
def test_cv_screening_does_not_use_nugget_tier_vocabulary(rel):
    offenders = forbidden_matches(_read(rel), TECH_TIERS)
    assert not offenders, (
        f"{rel} uses Nugget's tier vocabulary in executable code: {offenders}. "
        "CV screening tiers are shortlist / maybe / no_hire. A P1 here would imply "
        "a comparability between the two skills that does not exist."
    )


@pytest.mark.parametrize("rel", _existing(TECH_MODULES))
def test_technical_screening_does_not_use_cv_tier_vocabulary(rel):
    offenders = forbidden_matches(_read(rel), CV_TIERS)
    assert not offenders, (
        f"{rel} uses CV screening's tier vocabulary in executable code: {offenders}. "
        "Technical screening tiers are P1-P4 / MANUAL_REVIEW / UNUSABLE."
    )


# --- 4: distinct URL prefixes ----------------------------------------------


def test_the_two_routers_keep_distinct_prefixes():
    cv = _read("webapp/routers/cv_screening.py")
    assert 'prefix="/api/cv-screening"' in cv, "CV screening router prefix changed"

    tech_rel = "webapp/routers/tech_screening.py"
    if os.path.isfile(os.path.join(ROOT, tech_rel)):
        tech = _read(tech_rel)
        assert 'prefix="/api/tech-screening"' in tech, "tech screening router prefix changed"
        assert 'prefix="/api/cv-screening"' not in tech, (
            "technical screening is mounted on CV screening's prefix; the two would merge"
        )


# --- 5: the frontend pages stay separate ------------------------------------


def test_frontend_screening_pages_do_not_import_each_other():
    pairs = (
        ("frontend/src/pages/CVScreeningPage.tsx", ("TechScreeningPage", "EvaluationPage")),
        ("frontend/src/pages/TechScreeningPage.tsx", ("CVScreeningPage",)),
        ("frontend/src/pages/EvaluationPage.tsx", ("CVScreeningPage",)),
    )
    for rel, forbidden in pairs:
        path = os.path.join(ROOT, rel)
        if not os.path.isfile(path):
            continue
        source = _read(rel)
        imports = "\n".join(
            line for line in source.splitlines() if line.strip().startswith("import")
        )
        for name in forbidden:
            assert name not in imports, (
                f"{rel} imports {name}. The two screening pages must stay independent."
            )


# --- the gate proves itself: every checker fires on broken source -----------
# CLAUDE.md Rule 25. Without these, a checker that silently matched nothing
# would pass for ever and the protection would be imaginary.

_BROKEN_CV_IMPORT = "from ..services import nugget_writes\n"
_BROKEN_TECH_IMPORT = "from ..services.cv_screening import CRITERIA\n"
_BROKEN_CV_TABLE = 'SQL = "SELECT * FROM public.nugget_screening_evals"\n'
_BROKEN_TECH_TABLE = 'SQL = "INSERT INTO coco.cv_screens (match) VALUES (1)"\n'
_BROKEN_CV_TIER = 'def tier(x):\n    return "P1" if x > 85 else "MANUAL_REVIEW"\n'
_BROKEN_TECH_TIER = 'def tier(x):\n    return "shortlist" if x > 50 else "no_hire"\n'


def test_import_checker_fires_on_a_cv_module_importing_tech():
    offenders = forbidden_imports(_BROKEN_CV_IMPORT, TECH_ONLY_IMPORTS)
    assert any("nugget_writes" in name for name in offenders), (
        f"checker missed a real cross-import, saw {offenders}"
    )


def test_import_checker_fires_on_a_tech_module_importing_cv():
    assert forbidden_imports(_BROKEN_TECH_IMPORT, CV_ONLY_IMPORTS), (
        "checker missed a real cross-import"
    )


def test_table_checker_fires_on_nugget_sql_inside_cv_screening():
    assert forbidden_matches(_BROKEN_CV_TABLE, TECH_TABLES), "checker missed Nugget SQL"


def test_table_checker_fires_on_cv_sql_inside_technical_screening():
    assert forbidden_matches(_BROKEN_TECH_TABLE, CV_TABLES), "checker missed CV screen SQL"


def test_tier_checker_fires_on_nugget_tiers_inside_cv_screening():
    assert forbidden_matches(_BROKEN_CV_TIER, TECH_TIERS), "checker missed Nugget tiers"


def test_tier_checker_fires_on_cv_tiers_inside_technical_screening():
    assert forbidden_matches(_BROKEN_TECH_TIER, CV_TIERS), "checker missed CV tiers"


def test_gate_fires_on_the_real_module_once_it_is_broken():
    """The snippets above are small. This breaks the actual shipped file.

    A checker can pass on a toy and still miss the thing it was written for,
    so this takes cv_screening.py exactly as it is on disk, which the gate
    currently clears, adds one forbidden line, and asserts it now fails.
    """
    clean = _read("webapp/services/cv_screening.py")
    assert not forbidden_imports(clean, TECH_ONLY_IMPORTS)
    assert not forbidden_matches(clean, TECH_TABLES)
    assert not forbidden_matches(clean, TECH_TIERS)

    broken_import = clean + "\nfrom webapp.services import nugget_reads\n"
    assert forbidden_imports(broken_import, TECH_ONLY_IMPORTS), (
        "gate did not fire on the real module with a cross-import appended"
    )

    broken_sql = clean + '\n_Q = "SELECT tier FROM public.nugget_screening_evals"\n'
    assert forbidden_matches(broken_sql, TECH_TABLES), (
        "gate did not fire on the real module with Nugget SQL appended"
    )

    broken_tier = clean + '\n_T = "MANUAL_REVIEW"\n'
    assert forbidden_matches(broken_tier, TECH_TIERS), (
        "gate did not fire on the real module with a Nugget tier appended"
    )


def test_docstrings_are_exempt_so_the_separation_can_be_explained():
    """The thing that would make this gate unusable is a false positive.

    Both modules explain the separation in their docstring and name the other
    side's tables to do it. If that tripped the gate, the first fix anyone
    reached for would be deleting the explanation.
    """
    source = (
        '"""Not technical screening. That is public.nugget_screening_evals,\n'
        'scored P1-P4, read through nugget_reads."""\n'
        'SQL = "SELECT * FROM coco.cv_screens"\n'
    )
    assert not forbidden_matches(source, TECH_TABLES), "docstring wrongly flagged"
    assert not forbidden_matches(source, TECH_TIERS), "docstring wrongly flagged"


def test_comments_are_exempt_so_the_separation_can_be_explained():
    source = (
        "# Nugget scores P1-P4 against public.nugget_screening_evals. Not us.\n"
        'SQL = "SELECT * FROM coco.cv_screens"\n'
    )
    assert not forbidden_matches(source, TECH_TABLES), "comment wrongly flagged"
    assert not forbidden_matches(source, TECH_TIERS), "comment wrongly flagged"
