import uuid

from pytest_httpx import HTTPXMock

from tessera_sdk import TesseraClient


def test_delete_team(httpx_mock: HTTPXMock) -> None:
    team_id = uuid.uuid4()
    httpx_mock.add_response(
        url=f"http://test.local/api/v1/teams/{team_id}",
        method="DELETE",
        status_code=204,
    )

    with TesseraClient(base_url="http://test.local") as client:
        client.teams.delete(team_id)


def test_force_delete_team(httpx_mock: HTTPXMock) -> None:
    team_id = uuid.uuid4()
    httpx_mock.add_response(
        url=f"http://test.local/api/v1/teams/{team_id}?force=true",
        method="DELETE",
        status_code=204,
    )

    with TesseraClient(base_url="http://test.local") as client:
        client.teams.delete(team_id, force=True)


def test_restore_team(httpx_mock: HTTPXMock) -> None:
    team_id = uuid.uuid4()
    httpx_mock.add_response(
        url=f"http://test.local/api/v1/teams/{team_id}/restore",
        method="POST",
        json={
            "id": str(team_id),
            "name": "data-platform",
            "metadata": {},
            "created_at": "2024-01-01T00:00:00Z",
        },
    )

    with TesseraClient(base_url="http://test.local") as client:
        team = client.teams.restore(team_id)
        assert team.id == team_id
        assert team.name == "data-platform"


def test_reassign_assets(httpx_mock: HTTPXMock) -> None:
    team_id = uuid.uuid4()
    target_team = uuid.uuid4()
    assets = [uuid.uuid4(), uuid.uuid4()]
    httpx_mock.add_response(
        url=f"http://test.local/api/v1/teams/{team_id}/reassign-assets",
        method="POST",
        json={"status": "ok"},
    )

    with TesseraClient(base_url="http://test.local") as client:
        result = client.teams.reassign_assets(team_id, target_team, assets)
        assert result == {"status": "ok"}
