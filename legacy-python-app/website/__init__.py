# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, global-statement

from flask import Flask
from .views import views


def create_webapp() -> Flask:
    webapp = Flask(__name__, "/website/static")

    webapp.config['SECRET_KEY'] = "pythonisfun"  # 👍

    webapp.register_blueprint(views, url_prefix="/")

    return webapp
