from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="session")
def built():
    import app as entry

    return entry


@pytest.fixture()
def client(built):
    from starlette.testclient import TestClient

    import store

    store.reset()
    built.app.dispatch("bag.clear")
    wish = built.app.behavior.get("wish")
    wish.skus = ()
    return TestClient(built.asgi)
