from flask import Flask, jsonify

from app.repository import UserRepository
from app.routes import create_users_blueprint
from app.service import UserService


def create_app() -> Flask:
    app = Flask(__name__)

    repository = UserRepository()
    service = UserService(repository)
    app.register_blueprint(create_users_blueprint(service))

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app
