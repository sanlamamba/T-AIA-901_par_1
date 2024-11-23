from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api

db = SQLAlchemy()
migrate = Migrate()
api = Api(
    title='TOR API',
    version='1.0',
    description='TOR API for the T-AIA-901 project'
)
