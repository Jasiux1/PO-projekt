from datetime import date

import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_get_users_empty_list(client):
    response = client.get("/users")

    assert response.status_code == 200
    assert response.get_json() == []


def test_post_and_get_user(client):
    payload = {
        "firstName": "Jan",
        "lastName": "Nowak",
        "birthYear": 1995,
        "group": "premium",
    }

    create_response = client.post("/users", json=payload)
    assert create_response.status_code == 200

    created = create_response.get_json()
    assert created["id"] == 1
    assert created["age"] == date.today().year - 1995

    get_response = client.get("/users/1")
    assert get_response.status_code == 200
    assert get_response.get_json() == created


def test_patch_user(client):
    client.post(
        "/users",
        json={
            "firstName": "Jan",
            "lastName": "Nowak",
            "birthYear": 1995,
            "group": "user",
        },
    )

    patch_response = client.patch("/users/1", json={"group": "admin"})

    assert patch_response.status_code == 200
    assert patch_response.get_json()["group"] == "admin"


def test_delete_user(client):
    client.post(
        "/users",
        json={
            "firstName": "Jan",
            "lastName": "Nowak",
            "birthYear": 1995,
            "group": "user",
        },
    )

    delete_response = client.delete("/users/1")

    assert delete_response.status_code == 200
    assert delete_response.get_json()["id"] == 1

    get_after_delete = client.get("/users/1")
    assert get_after_delete.status_code == 404


def test_post_invalid_payload_returns_400(client):
    response = client.post(
        "/users",
        json={
            "firstName": "Jan",
            "lastName": "Nowak",
            "birthYear": 1995,
            "group": "vip",
        },
    )

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_patch_not_found_returns_404(client):
    response = client.patch("/users/999", json={"group": "admin"})

    assert response.status_code == 404


def test_patch_empty_payload_returns_400(client):
    client.post(
        "/users",
        json={
            "firstName": "Jan",
            "lastName": "Nowak",
            "birthYear": 1995,
            "group": "user",
        },
    )

    response = client.patch("/users/1", json={})

    assert response.status_code == 400


def test_patch_unsupported_field_returns_400(client):
    client.post(
        "/users",
        json={
            "firstName": "Jan",
            "lastName": "Nowak",
            "birthYear": 1995,
            "group": "user",
        },
    )

    response = client.patch("/users/1", json={"email": "jan@example.com"})

    assert response.status_code == 400


def test_invalid_json_returns_400(client):
    response = client.post(
        "/users",
        data="not-json",
        content_type="application/json",
    )

    assert response.status_code == 400
