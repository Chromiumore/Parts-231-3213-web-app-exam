from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint('recepies', __name__, url_prefix='/recepies')


def default():
    return redirect(url_for('recepies.index'))

@bp.route('/')
def index():
    return render_template('index.html')
