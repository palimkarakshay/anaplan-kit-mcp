"""Shared fixtures: pin content to the bundled snapshot, scrub all ANAPLAN_* env.

Every test runs against the package's own bundled content snapshot (so the
suite is self-contained — no anaplan-kit checkout needed in CI) and with a
guaranteed-clean credential environment.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from anaplan_kit_mcp import kitindex, live

BUNDLED_ROOT = Path(kitindex.__file__).resolve().parent / "_content"

_ALL_ENV = (
    kitindex.ENV_ROOT,
    live.ENV_EMAIL,
    live.ENV_PASSWORD,
    live.ENV_CERT_PATH,
    live.ENV_PRIVATE_KEY_PATH,
    live.ENV_PRIVATE_KEY_PASSWORD,
    live.ENV_WORKSPACE,
    live.ENV_MODEL,
)


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pin the kit root to the bundled snapshot; clear all Anaplan credentials."""
    for var in _ALL_ENV:
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv(kitindex.ENV_ROOT, str(BUNDLED_ROOT))


@pytest.fixture
def bundled_root() -> Path:
    return BUNDLED_ROOT
