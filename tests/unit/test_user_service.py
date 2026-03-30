from datetime import date

import pytest

from app.errors import NotFoundError, ValidationError
from app.repository import UserRepository
from app.service import UserService


@pytest.fixture
def service() -> UserService:
    return UserService(UserRepository())


def test_create_and_get_user(service: UserService):
    created = service.create_user(
        {
            "firstName": "Jan",
            "lastName": "Kowalski",
            "birthYear": 2000,
            "group": "user",
        }
    )

    assert created["id"] == 1
    assert created["firstName"] == "Jan"
    assert created["lastName"] == "Kowalski"
    assert created["age"] == date.today().year - 2000
    assert created["group"] == "user"

    fetched = service.get_user(1)
    assert fetched == created


def test_list_users_returns_all(service: UserService):
    service.create_user(
        {
            "firstName": "A",
            "lastName": "A",
            "birthYear": 1999,
            "group": "user",
        }
    )
    service.create_user(
        {
            "firstName": "B",
            "lastName": "B",
            "birthYear": 1998,
            "group": "premium",
        }
    )

    users = service.list_users()

    assert len(users) == 2
    assert users[0]["id"] == 1
    assert users[1]["id"] == 2


def test_create_user_invalid_group_raises_validation_error(service: UserService):
    with pytest.raises(ValidationError):
        service.create_user(
            {
                "firstName": "Jan",
                "lastName": "Kowalski",
                "birthYear": 2000,
                "group": "vip",
            }
        )


def test_create_user_with_extra_field_raises_validation_error(service: UserService):
    with pytest.raises(ValidationError):
        service.create_user(
            {
                "firstName": "Jan",
                "lastName": "Kowalski",
                "birthYear": 2000,
                "group": "user",
                "email": "jan@example.com",
            }
        )


def test_update_user_partial_data(service: UserService):
    service.create_user(
        {
            "firstName": "Jan",
            "lastName": "Kowalski",
            "birthYear": 2000,
            "group": "user",
        }
    )

    updated = service.update_user(1, {"group": "admin"})

    assert updated["group"] == "admin"
    assert updated["firstName"] == "Jan"


def test_delete_user_removes_it(service: UserService):
    service.create_user(
        {
            "firstName": "Jan",
            "lastName": "Kowalski",
            "birthYear": 2000,
            "group": "user",
        }
    )

    deleted = service.delete_user(1)
    assert deleted["id"] == 1

    with pytest.raises(NotFoundError):
        service.get_user(1)


def test_get_missing_user_raises_not_found(service: UserService):
    with pytest.raises(NotFoundError):
        service.get_user(999)
