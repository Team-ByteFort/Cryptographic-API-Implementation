from flask import Flask

from app.routes.encrypt_routes import encrypt_routes
from app.routes.hash_routes import hash_routes
from app.routes.key_routes import key_routes


def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(key_routes)
    app.register_blueprint(encrypt_routes)
    app.register_blueprint(hash_routes)

    return app
