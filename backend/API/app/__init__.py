from flask import Flask
from config import config
from .extensions import api
from .routes import register_routes
from flask_cors import CORS


def create_app(config_name):
    app = Flask(__name__, static_folder="static", static_url_path="/static")
    CORS(app)
    app.config.from_object(config[config_name])

    api.init_app(app)

    register_routes(api)

    return app
