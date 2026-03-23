from flask import Blueprint, jsonify, request

from app.errors import NotFoundError, ValidationError
from app.service import UserService


def create_users_blueprint(service: UserService) -> Blueprint:
    users_bp = Blueprint("users", __name__)

    @users_bp.get("/users")
    def get_users() -> tuple:
        return jsonify(service.list_users()), 200

    @users_bp.get("/users/<int:user_id>")
    def get_user(user_id: int) -> tuple:
        user = service.get_user(user_id)
        return jsonify(user), 200

    @users_bp.post("/users")
    def create_user() -> tuple:
        payload = request.get_json(silent=True)
        user = service.create_user(payload)
        return jsonify(user), 200

    @users_bp.patch("/users/<int:user_id>")
    def update_user(user_id: int) -> tuple:
        payload = request.get_json(silent=True)
        user = service.update_user(user_id, payload)
        return jsonify(user), 200

    @users_bp.delete("/users/<int:user_id>")
    def delete_user(user_id: int) -> tuple:
        user = service.delete_user(user_id)
        return jsonify(user), 200

    @users_bp.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        return jsonify({"error": str(error)}), 400

    @users_bp.errorhandler(NotFoundError)
    def handle_not_found_error(error: NotFoundError):
        return jsonify({"error": str(error)}), 404

    return users_bp
