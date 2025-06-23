from flask import Flask
from . import recipes, auth

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py', silent=False)

    app.register_blueprint(recipes.bp)
    app.route('/')(recipes.default)

    app.register_blueprint(auth.bp)

    return app
