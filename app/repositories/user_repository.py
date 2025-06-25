from hashlib import sha256
from sqlalchemy import and_
from app.models import User, Recipe, Feedback

class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_by_login_and_password(self, login, password):
        query = self.db.select(User).where(and_(User.login == login, sha256(password.encode()).hexdigest() == User.password_hash))
        return self.db.session.execute(query).scalar()

    def get(self, id):
        query = self.db.select(User).where(User.id == id)
        return self.db.session.execute(query).scalar()

    def get_recipe_author(self, recipe_id):
        query = self.db.select(User).join(Recipe, User.id == Recipe.user_id).where(Recipe.id == recipe_id)
        return self.db.session.execute(query).scalar()

    def get_feedback_author(self, feedback_id):
        query = self.db.select(User).join(Feedback, User.id == Feedback.user_id).where(Feedback.id == feedback_id)
        return self.db.session.execute(query).scalar()