from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint('recipes', __name__, url_prefix='/recipes')


def default():
    return redirect(url_for('recipes.index'))

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/view')
def view():
    return render_template('view-recipe.html')

@bp.route('/feedback')
def feedback():
    return render_template('feedback.html')

@bp.route('/new')
def new():
    return render_template('new-recipe.html')
