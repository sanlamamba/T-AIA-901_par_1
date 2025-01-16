from flask import Flask
from config import config
from .extensions import db, migrate, api
from .routes import register_routes

def create_app(config_name):
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    register_routes(api)

    return app
