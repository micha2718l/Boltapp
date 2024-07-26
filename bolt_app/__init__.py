from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from .routes import main
    from .commands import commands

    app.register_blueprint(main)
    app.register_blueprint(commands)

    return app
