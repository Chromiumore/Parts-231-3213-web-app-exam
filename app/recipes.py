import os
from uuid import uuid4
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash, abort, send_from_directory
from flask_login import login_required, current_user
from sqlalchemy.exc import DatabaseError
import bleach
from markdown import markdown
from .models import Recipe, db
from .repositories.file_repository import FileRepository, File
from .repositories.recipe_repository import RecipeRepository
from .repositories.user_repository import UserRepository
from .repositories.feedback_repository import FeedbackRepository, Feedback

bp = Blueprint('recipes', __name__, url_prefix='/recipes')

file_repository = FileRepository(db)
recipe_repository = RecipeRepository(db)
user_repository = UserRepository(db)
feedback_repository = FeedbackRepository(db)


def permission_required(only_admin=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated:
                user_id = current_user.id
                recipe = recipe_repository.get(kwargs.get('recipe_id'))
                feedback = feedback_repository.get(kwargs.get('feedback_id'))
                role_name = user_repository.get(user_id).get_role_name()
                print(recipe is None or recipe.user_id == user_id)
                if role_name == 'admin' or (((recipe.user_id == user_id and (feedback is None or feedback.user_id == user_id)) or (feedback is not None and feedback.user_id == user_id)) and not only_admin):
                    return func(*args, **kwargs)
                
                flash('У вас недостаточно прав для выполнения данного действия', 'warning')
                return redirect(url_for('recipes.index'))
        return wrapper
    return decorator


def default():
    return redirect(url_for('recipes.index'))

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    recipes = recipe_repository.all(page)
    return render_template('index.html', recipes=recipes)

@bp.route('/<int:recipe_id>')
def view(recipe_id):
    recipe = recipe_repository.get(recipe_id)
    if not recipe:
        abort(404)
    author = user_repository.get_recipe_author(recipe_id)
    feedbacks = feedback_repository.get_by_recipe(recipe_id, current_user.id if current_user.is_authenticated else None)
    feedbacks_info = [(fb, user_repository.get_feedback_author(fb.id)) for fb in feedbacks]
    files = list(file_repository.get_recipe_files(recipe.id))
    return render_template('view-recipe.html', recipe=recipe, author=author, feedbacks_info=feedbacks_info, files=files, markdown=markdown)

@bp.route('/new', methods=['POST', 'GET'])
@login_required
def new():
    if request.method == 'POST':
        try:
            form = request.form
            files = request.files.getlist('images')
            print(files)
            recipe = recipe_repository.create(
                Recipe(
                name=bleach.clean(form.get('name')),
                time=form.get('time'),
                portions=form.get('portions'),
                description=bleach.clean(form.get('description')),
                ingredients=bleach.clean(form.get('ingredients')),
                steps=bleach.clean(form.get('steps')),
                user_id=current_user.id
            )
            )

            f_objects = []

            for f in files:
                f_objects.append(File(
                    name = f"{uuid4()}-{f.filename}",
                    mime_type = f.mimetype,
                    recipe_id = recipe.id
                ))

            file_repository.create_files(f_objects)

            for i in range(len(files)):
                files[i].save(os.path.join(current_app.config['UPLOAD_FOLDER'], f_objects[i].name))

            flash('Рецепт успешно загружен', 'success')
            return redirect(url_for('recipes.index'))
        except DatabaseError as e:
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'danger')
            print(e)

    return render_template('new-recipe.html')

@bp.route('/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required()
def edit(recipe_id):
    recipe = recipe_repository.get(recipe_id)
    if not recipe:
        abort(404)
    if request.method == 'POST':
        try:
            form = request.form
            recipe_repository.update(recipe_id,
                Recipe(
                name=bleach.clean(form.get('name')),
                time=form.get('time'),
                portions=form.get('portions'),
                description=bleach.clean(form.get('description')),
                ingredients=bleach.clean(form.get('ingredients')),
                steps=bleach.clean(form.get('steps'))
            )
            )
            flash('Изменения успешно сохранены', 'success')
            return redirect(url_for('recipes.index'))
        except DatabaseError as e:
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'danger')
            print(e)

    return render_template('edit-recipe.html', recipe=recipe)

@bp.route('/<int:recipe_id>/delete', methods=['POST'])
@login_required
@permission_required()
def delete(recipe_id):
    recipe = recipe_repository.get(recipe_id)
    if not recipe:
        abort(404)

    recipe_files = file_repository.get_recipe_files(recipe_id)

    recipe_repository.delete(recipe_id)

    for file in recipe_files:
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], file.name))
    
    flash('Рецпт успешно удалён', 'success')

    return redirect(url_for('recipes.index'))

@bp.route('/<int:recipe_id>/feedback/new', methods=['POST', 'GET'])
@login_required
def new_feedback(recipe_id):
    recipe = recipe_repository.get(recipe_id)
    if not recipe:
        abort(404)

    if current_user.get_feedback(recipe_id):
        flash('Вы уже оставляли отзыв на данный рецепт.', 'warning')
        return redirect(url_for('recipes.view', recipe_id=recipe_id))

    if request.method == 'POST':
        try:
            form = request.form
            feedback_repository.create(
                Feedback(
                    recipe_id=recipe_id,
                    user_id=current_user.id,
                    rating=form.get('rating'),
                    feedback_text=bleach.clean(form.get('feedback_text'))
                )
            )
            flash('Отзыв успешно создан', 'success')
            return redirect(url_for('recipes.view', recipe_id=recipe_id))
        except DatabaseError as e:
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'danger')
    return render_template('new-feedback.html')

@bp.route('/<int:recipe_id>/feedback/<int:feedback_id>/edit', methods=['POST', 'GET'])
@login_required
@permission_required()
def edit_feedback(recipe_id, feedback_id):
    recipe = recipe_repository.get(recipe_id)
    feedback = feedback_repository.get(feedback_id)
    if not recipe or not feedback:
        abort(404)

    if request.method == 'POST':
        try:
            form = request.form
            feedback_repository.update(feedback_id,
                Feedback(
                    recipe_id=recipe_id,
                    user_id=current_user.id,
                    rating=form.get('rating'),
                    feedback_text=bleach.clean(form.get('feedback_text'))
                )
            )
            flash('Отзыв успешно изменён', 'success')
            return redirect(url_for('recipes.view', recipe_id=recipe_id))
        except DatabaseError as e:
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'danger')
    return render_template('edit-feedback.html', feedback=feedback_repository.get(feedback_id))

@bp.route('/<int:recipe_id>/feedback/<int:feedback_id>/delete', methods=['POST'])
@login_required
@permission_required()
def delete_feedback(recipe_id, feedback_id):
    recipe = recipe_repository.get(recipe_id)
    feedback = feedback_repository.get(feedback_id)
    if not recipe or not feedback:
        abort(404)
        
    feedback_repository.delete(feedback_id)

    flash('Отзыв успешно удалён', 'success')
            
    return redirect(url_for('recipes.view', recipe_id=recipe_id))

@bp.route('/uploads/<filename>')
def send_uploaded_file(filename):
    file = file_repository.get_file_by_filename(filename)
    if not file:
        abort(404)
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], file.name)
