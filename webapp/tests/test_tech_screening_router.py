"""Gates on the technical screening wizard.

Run: python -m pytest webapp/tests/test_tech_screening_router.py -v

This router writes into tables holding 863 live evaluations, so the question
"which of these endpoints can a viewer reach" has to be answered by the tree
FastAPI actually resolves, not by reading the decorators and trusting them.
"""

from __future__ import annotations

import pytest

from webapp import deps
from webapp.routers import tech_screening as router_mod


def _dependencies(path: str, method: str) -> set:
    """The dependency CALLABLES FastAPI resolves for this route.

    Identity, not names. `require_editor`, `require_approver` and
    `require_super_admin` are all closures produced by `deps._require_role`, so
    each is named `dep` and a name-based assertion would pass on any of them.

    Read off `router_mod.router.routes`, because this FastAPI wraps every
    included router in an opaque `_IncludedRouter` that exposes no paths.
    """
    for route in router_mod.router.routes:
        if getattr(route, "path", None) == path and method in (
            getattr(route, "methods", None) or set()
        ):
            return {d.call for d in route.dependant.dependencies if getattr(d, "call", None)}
    raise AssertionError(f"route not found: {method} {path}")


# Every endpoint that writes to Nugget's tables, or spends money.
WRITE_ROUTES = [
    ("/api/tech-screening/rubric/draft", "POST"),   # spends a model call
    ("/api/tech-screening/rubric", "POST"),         # publishes a rubric
    ("/api/tech-screening/runs", "POST"),           # creates a run
    ("/api/tech-screening/runs/{run_id}/work", "POST"),   # scores candidates
    ("/api/tech-screening/runs/{run_id}/cancel", "POST"),
]

READ_ROUTES = [
    ("/api/tech-screening/jobs", "GET"),
    ("/api/tech-screening/models", "GET"),
    ("/api/tech-screening/jobs/{job_id}/rubric", "GET"),
    ("/api/tech-screening/runs/plan", "POST"),      # reads only, by design
    ("/api/tech-screening/runs/{run_id}", "GET"),
    ("/api/tech-screening/jobs/{job_id}/runs", "GET"),
]


@pytest.mark.parametrize("path,method", WRITE_ROUTES)
def test_write_routes_require_editor(path, method):
    assert deps.require_editor in _dependencies(path, method), (
        f"{method} {path} writes to Nugget's tables or spends money and must "
        "be gated on require_editor"
    )


@pytest.mark.parametrize("path,method", READ_ROUTES)
def test_read_routes_require_a_signed_in_user(path, method):
    deps_found = _dependencies(path, method)
    assert deps.get_current_user in deps_found or deps.require_editor in deps_found


def test_the_gate_assertion_bites():
    """Proof the check is load-bearing: a route with no editor gate must fail
    it. Without this, a bug in `_dependencies` would make every test above
    pass while checking nothing."""
    assert deps.require_editor not in _dependencies("/api/tech-screening/jobs", "GET")


def test_plan_writes_nothing():
    """Step 3 shows the pool and the cost before anyone commits to spending.
    It is the one POST here that is deliberately read-only, so it must not
    reach for the writer."""
    import inspect

    source = inspect.getsource(router_mod.plan)
    assert "nugget_writes" not in source
    assert "db.commit" not in source


def test_every_write_route_rolls_back_on_failure():
    """A half-written run or rubric is worse than none: `uq_nsr_active_per_job`
    means a failed publish that archived the old rubric without inserting the
    new one leaves the job with NO active rubric, which every other query reads
    as 'never screened'."""
    import inspect

    for name in ("publish_rubric", "create_run", "work", "cancel_run"):
        source = inspect.getsource(getattr(router_mod, name))
        assert "db.rollback()" in source, f"{name} does not roll back on failure"


def test_the_router_does_not_touch_cocos_cv_screening():
    """Coco's CV screening is a separate system with its own criteria and its
    own shortlist/maybe/no_hire vocabulary. The two must never share a rubric
    or a tier (Ayesha, 2026-09-15).

    Checked against the CODE, not the file text: this module's docstring names
    that boundary on purpose, and a raw substring scan flags the very comment
    that documents the rule it is enforcing.
    """
    import ast
    import inspect

    tree = ast.parse(inspect.getsource(router_mod))

    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            imported.update(a.name for a in node.names)
        elif isinstance(node, ast.Import):
            imported.update(a.name for a in node.names)
    assert "cv_screening" not in imported, (
        "the technical screening router must not import Coco's CV screening"
    )

    literals = {
        n.value for n in ast.walk(tree)
        if isinstance(n, ast.Constant) and isinstance(n.value, str)
    }
    # Docstrings are string constants too, so compare only short, code-like
    # ones: a tier label appearing as a value is the thing that would matter.
    for banned in ("shortlist", "maybe", "no_hire"):
        assert banned not in {s for s in literals if len(s) < 40}, (
            f"{banned!r} is Coco's CV-screening vocabulary, not Nugget's"
        )
