from flask import Flask
from app.routes.key_routes import key_routes
from app.routes.encrypt_routes import encrypt_routes
from app.routes.hash_routes import hash_routes

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(key_routes, url_prefix='/key')
    app.register_blueprint(encrypt_routes, url_prefix='/encrypt')
    app.register_blueprint(hash_routes, url_prefix='/hash')

    return app
