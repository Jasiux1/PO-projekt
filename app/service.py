from datetime import date

from app.errors import NotFoundError, ValidationError
from app.repository import UserRepository


ALLOWED_GROUPS = {"user", "premium", "admin"}


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def list_users(self) -> list[dict]:
        users = self._repository.list_users()
        users = sorted(users, key=lambda user: user["id"])
        return [self._to_response(user) for user in users]

    def get_user(self, user_id: int) -> dict:
        self._validate_user_id(user_id)
        user = self._repository.get_user(user_id)
        if user is None:
            raise NotFoundError("User not found")
        return self._to_response(user)

    def create_user(self, payload: dict) -> dict:
        validated = self._validate_create_payload(payload)
        created = self._repository.create_user(validated)
        return self._to_response(created)

    def update_user(self, user_id: int, payload: dict) -> dict:
        self._validate_user_id(user_id)
        updates = self._validate_patch_payload(payload)

        updated = self._repository.update_user(user_id, updates)
        if updated is None:
            raise NotFoundError("User not found")

        return self._to_response(updated)

    def delete_user(self, user_id: int) -> dict:
        self._validate_user_id(user_id)
        deleted = self._repository.delete_user(user_id)
        if deleted is None:
            raise NotFoundError("User not found")

        return self._to_response(deleted)

    def _validate_user_id(self, user_id: int) -> None:
        if type(user_id) is not int or user_id <= 0:
            raise ValidationError("id must be a positive integer")

    def _validate_create_payload(self, payload: dict) -> dict:
        if type(payload) is not dict:
            raise ValidationError("payload must be a JSON object")

        required_keys = {"firstName", "lastName", "birthYear", "group"}
        if set(payload.keys()) != required_keys:
            raise ValidationError("payload must contain exactly: firstName, lastName, birthYear, group")

        return {
            "firstName": self._validate_name(payload["firstName"], "firstName"),
            "lastName": self._validate_name(payload["lastName"], "lastName"),
            "birthYear": self._validate_birth_year(payload["birthYear"]),
            "group": self._validate_group(payload["group"]),
        }

    def _validate_patch_payload(self, payload: dict) -> dict:
        if type(payload) is not dict:
            raise ValidationError("payload must be a JSON object")

        if not payload:
            raise ValidationError("payload cannot be empty")

        allowed_keys = {"firstName", "lastName", "birthYear", "group"}
        if not set(payload.keys()).issubset(allowed_keys):
            raise ValidationError("payload contains unsupported fields")

        updates = {}
        if "firstName" in payload:
            updates["firstName"] = self._validate_name(payload["firstName"], "firstName")
        if "lastName" in payload:
            updates["lastName"] = self._validate_name(payload["lastName"], "lastName")
        if "birthYear" in payload:
            updates["birthYear"] = self._validate_birth_year(payload["birthYear"])
        if "group" in payload:
            updates["group"] = self._validate_group(payload["group"])

        return updates

    def _validate_name(self, value: object, field_name: str) -> str:
        if type(value) is not str:
            raise ValidationError(f"{field_name} must be a string")

        normalized = value.strip()
        if not normalized:
            raise ValidationError(f"{field_name} cannot be empty")

        return normalized

    def _validate_birth_year(self, value: object) -> int:
        current_year = date.today().year
        if type(value) is not int:
            raise ValidationError("birthYear must be an integer")
        if value < 1900 or value > current_year:
            raise ValidationError("birthYear is out of allowed range")
        return value

    def _validate_group(self, value: object) -> str:
        if type(value) is not str:
            raise ValidationError("group must be a string")

        if value not in ALLOWED_GROUPS:
            raise ValidationError("group must be one of: user, premium, admin")

        return value

    def _to_response(self, user: dict) -> dict:
        return {
            "id": user["id"],
            "firstName": user["firstName"],
            "lastName": user["lastName"],
            "age": date.today().year - user["birthYear"],
            "group": user["group"],
        }
