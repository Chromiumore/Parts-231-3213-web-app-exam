from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from .repositories.user_repository import UserRepository
from .models import db

user_repository = UserRepository(db)

bp = Blueprint('auth', __name__, url_prefix='/auth')


def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Для доступа к данной странице необходимо пройти процедуру аутентификации.'
    login_manager.login_message_category = 'warning'
    login_manager.user_loader(load_user)
    login_manager.init_app(app)

def load_user(user_id):
    return user_repository.get(user_id)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('recipes.index')
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me')
        if login and password:
            user = user_repository.get_by_login_and_password(login, password)
            if user:
                login_user(user, remember=remember_me)
                flash('Вы были успешно авторизованы', 'success')
                return redirect(url_for('recipes.index'))
        flash('Невозможно аутентифицироваться с указанными логином и паролем. Попробуйте ещё раз. ', 'danger')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('recipes.index'))
