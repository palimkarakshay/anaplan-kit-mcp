"""Tests for the live Anaplan API tools — all offline, anaplan-sdk mocked at the
client-interface level (fakes/monkeypatching, never live calls).

The load-bearing honesty invariant is asserted explicitly: with no credentials
configured every live tool returns the structured offline answer WITHOUT
raising and WITHOUT importing the SDK (so no network attempt is even possible).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from anaplan_kit_mcp import live, server

ALL_LIVE_CALLS = (
    lambda: server.anaplan_list_workspaces(),
    lambda: server.anaplan_list_models(workspace_id="ws123"),
    lambda: server.anaplan_model_metadata(model_id="m456", workspace_id="ws123"),
    lambda: server.anaplan_run_action("117000000001", workspace_id="ws123", model_id="m456"),
    lambda: server.anaplan_run_import("112000000001", workspace_id="ws123", model_id="m456"),
    lambda: server.anaplan_run_export("116000000001", workspace_id="ws123", model_id="m456"),
    lambda: server.anaplan_run_process("118000000001", workspace_id="ws123", model_id="m456"),
)


def _set_basic_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(live.ENV_EMAIL, "tester@example.com")
    monkeypatch.setenv(live.ENV_PASSWORD, "secret-value")  # noqa: S105 - dummy test value


# --- fakes -------------------------------------------------------------------


class FakeDumpable:
    """Mimics a pydantic model: carries data, exposes model_dump()."""

    def __init__(self, **data: Any) -> None:
        self._data = data

    def model_dump(self) -> dict[str, Any]:
        return dict(self._data)


class FakeTransactional:
    def get_modules(self):
        return [FakeDumpable(id=101, name="CAL01 Revenue")]

    def get_lists(self):
        return [FakeDumpable(id=201, name="Products")]


class FakeClient:
    """A stand-in for anaplan_sdk.Client at the interface the server uses."""

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs
        self.run_calls: list[int] = []

    def get_workspaces(self):
        return [FakeDumpable(id="ws123", name="WS")]

    def get_models(self, only_in_workspace: bool | str = False):
        self.models_filter = only_in_workspace
        return [FakeDumpable(id="m456", name="Model")]

    def get_files(self):
        return [FakeDumpable(id=113000000001, name="data.csv")]

    def get_imports(self):
        return [FakeDumpable(id=112000000001, name="Import data")]

    def get_exports(self):
        return [FakeDumpable(id=116000000001, name="Export data")]

    def get_actions(self):
        return [FakeDumpable(id=117000000001, name="Delete old")]

    def get_processes(self):
        return [FakeDumpable(id=118000000001, name="Nightly load")]

    @property
    def tr(self) -> FakeTransactional:
        return FakeTransactional()

    def run_action(self, action_id: int, wait_for_completion: bool = True):
        self.run_calls.append(action_id)
        return FakeDumpable(task_id="t1", task_state="COMPLETE")


@pytest.fixture
def fake_client(monkeypatch: pytest.MonkeyPatch) -> FakeClient:
    """Route server tools at one FakeClient instance (creds implicitly 'set')."""
    client = FakeClient()
    monkeypatch.setattr(live, "make_client", lambda *a, **k: (client, None))
    return client


# --- offline honesty invariant (load-bearing) ----------------------------------


def test_live_tools_return_offline_without_creds(monkeypatch: pytest.MonkeyPatch) -> None:
    def _boom() -> None:  # the SDK must never even be imported on this path
        raise AssertionError("anaplan-sdk import attempted without credentials")

    monkeypatch.setattr(live, "_import_sdk", _boom)
    for call in ALL_LIVE_CALLS:
        result = call()
        assert result["mode"] == "offline"
        assert result["error"] == "no Anaplan credentials configured"


def test_offline_response_is_exact_contract() -> None:
    result = server.anaplan_list_workspaces()
    assert result["mode"] == "offline"
    assert result["error"] == "no Anaplan credentials configured"
    assert "hint" in result


def test_sdk_missing_with_creds_mentions_live_extra(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_basic_env(monkeypatch)
    monkeypatch.setattr(live, "_import_sdk", lambda: None)
    result = server.anaplan_list_workspaces()
    assert result["mode"] == "offline"
    assert "anaplan-sdk" in result["error"]
    assert "[live]" in result["error"]


# --- connection status -----------------------------------------------------------


def test_connection_status_offline_without_creds() -> None:
    status = server.anaplan_connection_status()
    assert status["mode"] == "offline"
    assert status["auth_method"] is None
    assert status["configured"][live.ENV_EMAIL] is False


def test_connection_status_never_reveals_values(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_basic_env(monkeypatch)
    monkeypatch.setattr(live, "sdk_available", lambda: True)
    status = server.anaplan_connection_status()
    assert status["mode"] == "live"
    assert status["auth_method"] == "basic"
    assert status["configured"][live.ENV_PASSWORD] is True
    assert "secret-value" not in str(status)
    assert "tester@example.com" not in str(status)


def test_connection_status_certificate_auth(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv(live.ENV_CERT_PATH, str(tmp_path / "cert.pem"))
    monkeypatch.setenv(live.ENV_PRIVATE_KEY_PATH, str(tmp_path / "key.pem"))
    monkeypatch.setattr(live, "sdk_available", lambda: True)
    status = server.anaplan_connection_status()
    assert status["mode"] == "live"
    assert status["auth_method"] == "certificate"


def test_connection_status_creds_but_no_sdk_is_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_basic_env(monkeypatch)
    monkeypatch.setattr(live, "sdk_available", lambda: False)
    status = server.anaplan_connection_status()
    assert status["mode"] == "offline"
    assert status["sdk_installed"] is False
    assert "[live]" in status["hint"]


# --- client construction (fake SDK module) -----------------------------------------


class FakeSdkModule:
    """Stands in for the imported anaplan_sdk module; records Client kwargs."""

    def __init__(self) -> None:
        self.client_kwargs: dict[str, Any] | None = None
        outer = self

        class Client:
            def __init__(self, **kwargs: Any) -> None:
                outer.client_kwargs = kwargs

        self.Client = Client


def test_make_client_passes_basic_auth_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_basic_env(monkeypatch)
    fake_sdk = FakeSdkModule()
    monkeypatch.setattr(live, "_import_sdk", lambda: fake_sdk)
    client, err = live.make_client(workspace_id="ws1", model_id="m1")
    assert err is None and client is not None
    assert fake_sdk.client_kwargs == {
        "workspace_id": "ws1",
        "model_id": "m1",
        "user_email": "tester@example.com",
        "password": "secret-value",
    }


def test_make_client_prefers_certificate_auth(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _set_basic_env(monkeypatch)  # both methods set: certificate must win
    cert, key = tmp_path / "cert.pem", tmp_path / "key.pem"
    monkeypatch.setenv(live.ENV_CERT_PATH, str(cert))
    monkeypatch.setenv(live.ENV_PRIVATE_KEY_PATH, str(key))
    fake_sdk = FakeSdkModule()
    monkeypatch.setattr(live, "_import_sdk", lambda: fake_sdk)
    client, err = live.make_client()
    assert err is None and client is not None
    assert fake_sdk.client_kwargs["certificate"] == str(cert)
    assert fake_sdk.client_kwargs["private_key"] == str(key)
    assert "password" not in fake_sdk.client_kwargs


def test_make_client_construction_failure_is_structured(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_basic_env(monkeypatch)

    class ExplodingSdk:
        class Client:
            def __init__(self, **kwargs: Any) -> None:
                raise ValueError("bad certificate")

    monkeypatch.setattr(live, "_import_sdk", lambda: ExplodingSdk())
    client, err = live.make_client()
    assert client is None
    assert err["mode"] == "offline"
    assert "bad certificate" in err["error"]


# --- live happy paths (fake client) -------------------------------------------------


def test_list_workspaces_live(fake_client: FakeClient) -> None:
    result = server.anaplan_list_workspaces()
    assert result["mode"] == "live"
    assert result["workspaces"][0]["id"] == "ws123"


def test_list_models_live_uses_env_workspace(
    fake_client: FakeClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(live.ENV_WORKSPACE, "ws123")
    result = server.anaplan_list_models()
    assert result["mode"] == "live"
    assert result["workspace_id"] == "ws123"
    assert fake_client.models_filter == "ws123"
    assert result["models"][0]["id"] == "m456"


def test_list_models_without_workspace_lists_all(fake_client: FakeClient) -> None:
    result = server.anaplan_list_models()
    assert result["mode"] == "live"
    assert result["workspace_id"] is None
    assert fake_client.models_filter is False


def test_model_metadata_live(fake_client: FakeClient) -> None:
    result = server.anaplan_model_metadata(model_id="m456", workspace_id="ws123")
    assert result["mode"] == "live"
    assert result["imports"][0]["id"] == 112000000001
    assert result["processes"][0]["name"] == "Nightly load"
    assert result["modules"][0]["name"] == "CAL01 Revenue"
    assert result["lists"][0]["name"] == "Products"
    assert "transactional_error" not in result


def test_model_metadata_missing_ids_is_structured(fake_client: FakeClient) -> None:
    result = server.anaplan_model_metadata()
    assert result["mode"] == "live"
    assert live.ENV_WORKSPACE in result["error"]


def test_model_metadata_transactional_failure_keeps_bulk(
    fake_client: FakeClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    def _raise(self) -> None:
        raise ValueError("no model_id bound")

    monkeypatch.setattr(FakeClient, "tr", property(_raise))
    result = server.anaplan_model_metadata(model_id="m456", workspace_id="ws123")
    assert result["mode"] == "live"
    assert result["files"]  # bulk metadata survived
    assert result["modules"] is None
    assert "no model_id bound" in result["transactional_error"]


def test_run_process_live(fake_client: FakeClient) -> None:
    result = server.anaplan_run_process("118000000001", workspace_id="ws123", model_id="m456")
    assert result["mode"] == "live"
    assert result["resource"] == "process"
    assert result["task"]["task_state"] == "COMPLETE"
    assert fake_client.run_calls == [118000000001]


def test_run_import_uses_env_ids(fake_client: FakeClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(live.ENV_WORKSPACE, "ws-env")
    monkeypatch.setenv(live.ENV_MODEL, "m-env")
    result = server.anaplan_run_import("112000000001")
    assert result["mode"] == "live"
    assert result["workspace_id"] == "ws-env"
    assert result["model_id"] == "m-env"


def test_run_action_missing_model_is_structured(fake_client: FakeClient) -> None:
    result = server.anaplan_run_action("117000000001", workspace_id="ws123")
    assert result["mode"] == "live"
    assert live.ENV_MODEL in result["error"]


def test_run_action_non_numeric_id_is_structured(fake_client: FakeClient) -> None:
    result = server.anaplan_run_action("not-a-number", workspace_id="ws123", model_id="m456")
    assert result["mode"] == "live"
    assert "numeric" in result["error"]
    assert fake_client.run_calls == []


def test_live_api_error_is_structured_not_raised(
    fake_client: FakeClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    def _boom(self) -> None:
        raise RuntimeError("403 forbidden")

    monkeypatch.setattr(FakeClient, "get_workspaces", _boom)
    result = server.anaplan_list_workspaces()
    assert result["mode"] == "live"
    assert "403 forbidden" in result["error"]
