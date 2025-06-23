from flask import Flask
import app.recipes

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py', silent=False)

    app.register_blueprint(recipes.bp)
    app.route('/')(recipes.default)

    return app
