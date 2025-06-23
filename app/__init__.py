from flask import Flask
import app.recepies

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py', silent=False)

    app.register_blueprint(recepies.bp)
    app.route('/')(recepies.default)

    return app
