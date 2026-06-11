"""Live Anaplan API access built on `anaplan-sdk <https://github.com/VinzenzKlass/anaplan-sdk>`_.

The SDK is an **optional dependency** (the ``[live]`` extra). Credentials come
from environment variables only — basic auth (``ANAPLAN_EMAIL`` /
``ANAPLAN_PASSWORD``) or certificate auth (``ANAPLAN_CERT_PATH`` /
``ANAPLAN_PRIVATE_KEY_PATH``). Values are never hardcoded and never logged.

**Offline honesty invariant (load-bearing):** when no credentials are
configured, :func:`make_client` returns a structured
``{"mode": "offline", "error": "no Anaplan credentials configured"}`` response
WITHOUT raising and WITHOUT importing the SDK or attempting any network I/O.
When credentials are set but anaplan-sdk is not installed, the same structured
offline response points at the ``[live]`` extra. The server must start and
serve every offline tool with zero credentials and zero network.
"""

from __future__ import annotations

import importlib.util
import os
from typing import Any

ENV_EMAIL = "ANAPLAN_EMAIL"
ENV_PASSWORD = "ANAPLAN_PASSWORD"  # noqa: S105 - env var *name*, not a secret
ENV_CERT_PATH = "ANAPLAN_CERT_PATH"
ENV_PRIVATE_KEY_PATH = "ANAPLAN_PRIVATE_KEY_PATH"
ENV_PRIVATE_KEY_PASSWORD = "ANAPLAN_PRIVATE_KEY_PASSWORD"  # noqa: S105
ENV_WORKSPACE = "ANAPLAN_WORKSPACE_ID"
ENV_MODEL = "ANAPLAN_MODEL_ID"

NO_CREDENTIALS = "no Anaplan credentials configured"
LIVE_EXTRA_HINT = "pip install 'anaplan-kit-mcp[live]'"


def _import_sdk() -> Any | None:
    """Import anaplan_sdk lazily; ``None`` when the [live] extra is absent."""
    try:
        import anaplan_sdk
    except ImportError:
        return None
    return anaplan_sdk


def sdk_available() -> bool:
    """True when anaplan-sdk is installed (checked without importing it)."""
    return importlib.util.find_spec("anaplan_sdk") is not None


def credentials_kwargs() -> dict[str, str] | None:
    """anaplan-sdk ``Client`` auth kwargs from the environment, or ``None``.

    Certificate auth wins when both auth methods are configured (mirroring the
    SDK's own precedence). Returns ``None`` when neither is fully configured.
    """
    cert = os.environ.get(ENV_CERT_PATH)
    key = os.environ.get(ENV_PRIVATE_KEY_PATH)
    if cert and key:
        kwargs = {"certificate": cert, "private_key": key}
        key_password = os.environ.get(ENV_PRIVATE_KEY_PASSWORD)
        if key_password:
            kwargs["private_key_password"] = key_password
        return kwargs
    email = os.environ.get(ENV_EMAIL)
    password = os.environ.get(ENV_PASSWORD)
    if email and password:
        return {"user_email": email, "password": password}
    return None


def resolved_ids(
    workspace_id: str | None, model_id: str | None = None
) -> tuple[str | None, str | None]:
    """Fill missing workspace/model IDs from the environment."""
    return (
        workspace_id or os.environ.get(ENV_WORKSPACE) or None,
        model_id or os.environ.get(ENV_MODEL) or None,
    )


# --- structured (never-raising) responses ------------------------------------


def offline_response() -> dict[str, Any]:
    """The structured no-credentials answer every live tool must return."""
    return {
        "mode": "offline",
        "error": NO_CREDENTIALS,
        "hint": (
            f"set {ENV_EMAIL}+{ENV_PASSWORD} (basic auth) or "
            f"{ENV_CERT_PATH}+{ENV_PRIVATE_KEY_PATH} (certificate auth) "
            "in the server's environment to go live"
        ),
    }


def sdk_missing_response() -> dict[str, Any]:
    """Structured answer when credentials are set but the SDK is absent."""
    return {
        "mode": "offline",
        "error": f"anaplan-sdk is not installed — install the [live] extra: {LIVE_EXTRA_HINT}",
    }


def live_error(exc: Exception) -> dict[str, Any]:
    """A structured (never-raising) report of a live API failure."""
    return {"mode": "live", "error": f"{type(exc).__name__}: {exc}"}


def missing_id_error(name: str, env_var: str) -> dict[str, Any]:
    return {
        "mode": "live",
        "error": f"missing {name}: pass it as an argument or set {env_var}",
    }


# --- client construction -------------------------------------------------------


def make_client(
    workspace_id: str | None = None, model_id: str | None = None
) -> tuple[Any | None, dict[str, Any] | None]:
    """An anaplan-sdk ``Client`` from env credentials, or a structured error.

    Returns ``(client, None)`` on success or ``(None, response)`` where
    ``response`` is the offline/error dict the tool should return verbatim.
    Credentials are checked **before** the SDK import, so a credential-less
    process never even imports anaplan-sdk. Construction performs no network
    I/O — the SDK authenticates lazily on the first API call.
    """
    creds = credentials_kwargs()
    if creds is None:
        return None, offline_response()
    sdk = _import_sdk()
    if sdk is None:
        return None, sdk_missing_response()
    try:
        client = sdk.Client(workspace_id=workspace_id, model_id=model_id, **creds)
    except Exception as exc:  # e.g. unreadable certificate file — never raise
        return None, {
            "mode": "offline",
            "error": f"could not initialise the anaplan-sdk client: {type(exc).__name__}: {exc}",
        }
    return client, None


def connection_status() -> dict[str, Any]:
    """Report credential/SDK configuration without revealing any values."""
    configured = {
        ENV_EMAIL: bool(os.environ.get(ENV_EMAIL)),
        ENV_PASSWORD: bool(os.environ.get(ENV_PASSWORD)),
        ENV_CERT_PATH: bool(os.environ.get(ENV_CERT_PATH)),
        ENV_PRIVATE_KEY_PATH: bool(os.environ.get(ENV_PRIVATE_KEY_PATH)),
        ENV_WORKSPACE: bool(os.environ.get(ENV_WORKSPACE)),
        ENV_MODEL: bool(os.environ.get(ENV_MODEL)),
    }
    basic = configured[ENV_EMAIL] and configured[ENV_PASSWORD]
    certificate = configured[ENV_CERT_PATH] and configured[ENV_PRIVATE_KEY_PATH]
    sdk = sdk_available()
    status: dict[str, Any] = {
        "mode": "live" if ((basic or certificate) and sdk) else "offline",
        "auth_method": "certificate" if certificate else ("basic" if basic else None),
        "sdk_installed": sdk,
        "configured": configured,
        "note": "credential values are never revealed; without credentials the live "
        "tools return mode=offline instead of contacting Anaplan",
    }
    if (basic or certificate) and not sdk:
        status["hint"] = f"credentials are set but anaplan-sdk is missing: {LIVE_EXTRA_HINT}"
    return status


# --- result serialization --------------------------------------------------------


def dump_one(obj: Any) -> Any:
    """JSON-friendly form of one SDK result (pydantic models -> dicts)."""
    model_dump = getattr(obj, "model_dump", None)
    if callable(model_dump):
        return model_dump()
    return obj


def dump(items: Any) -> list[Any]:
    """JSON-friendly form of a list of SDK results."""
    return [dump_one(item) for item in items]
