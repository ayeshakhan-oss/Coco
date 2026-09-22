"""Shared state and policy for the pytest DDL guard installed by conftest.py.

This lives in a normal module rather than in conftest.py because pytest imports
conftest.py under its own module identity. `from webapp.tests.conftest import
BLOCKED_DDL` therefore builds a SECOND copy of that module with its own empty
list, and a test asserting on it silently sees nothing -- which is exactly what
happened on the first run of test_ddl_guard.py: the guard fired and logged, and
the assertion still failed. One module, one list.

See conftest.py for why the guard exists at all.
"""

from __future__ import annotations

import os
from typing import Any, Optional

#: Set to "1" to permit DDL against a real database during a test run.
ALLOW_ENV = "COCO_ALLOW_TEST_DDL"

#: Every DDL attempt this session blocked, as (operation, url).
BLOCKED_DDL: list[tuple[str, str]] = []


def ddl_is_allowed(url: Optional[str]) -> bool:
    """True if DDL may be executed against `url` during a test run.

    SQLite is a scratch database. Anything else needs a deliberate opt-in. A
    missing URL is allowed through because get_engine() raises RuntimeError on
    its own and that pre-existing behaviour is not ours to swallow.
    """
    if os.environ.get(ALLOW_ENV) == "1":
        return True
    if not url:
        return True
    return url.lower().startswith("sqlite")


def bind_url(bind: Any) -> Optional[str]:
    """The URL a create_all() bind points at, or None if it has no URL."""
    try:
        return str(bind.url)
    except AttributeError:
        return None
