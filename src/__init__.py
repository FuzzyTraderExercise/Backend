import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta

db = SQLAlchemy()


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)

    # register blueprints
    from src.routes.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    # set up jwt token
    jwt = JWTManager(app)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES'))
    )
    app.config['JWT_SECRET_KEY'] =  os.getenv('JWT_SECRET_KEY')

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
