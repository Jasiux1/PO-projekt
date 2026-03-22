from copy import deepcopy


class UserRepository:
    def __init__(self) -> None:
        self._users: dict[int, dict] = {}
        self._next_id: int = 1

    def list_users(self) -> list[dict]:
        users = sorted(self._users.values(), key=lambda user: user["id"])
        return [deepcopy(user) for user in users]

    def get_user(self, user_id: int) -> dict | None:
        user = self._users.get(user_id)
        if user is None:
            return None
        return deepcopy(user)

    def create_user(self, user_data: dict) -> dict:
        user_id = self._next_id
        self._next_id += 1

        saved_user = deepcopy(user_data)
        saved_user["id"] = user_id
        self._users[user_id] = saved_user
        return deepcopy(saved_user)

    def update_user(self, user_id: int, updates: dict) -> dict | None:
        if user_id not in self._users:
            return None

        self._users[user_id].update(deepcopy(updates))
        return deepcopy(self._users[user_id])

    def delete_user(self, user_id: int) -> dict | None:
        user = self._users.pop(user_id, None)
        if user is None:
            return None
        return deepcopy(user)
