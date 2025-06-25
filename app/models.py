from datetime import date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData, String, ForeignKey, Text, Integer, func
from sqlalchemy.ext.hybrid import hybrid_method
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

db = SQLAlchemy(model_class=Base)

class User(Base, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(40))
    password_hash: Mapped[str] = mapped_column(String(256))
    surname: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(50))
    middle_name: Mapped[str] = mapped_column(String(50), nullable=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))

    @hybrid_method
    def get_role_name(self):
        return db.session.query(Role.name).join(User).where(User.id == self.id).scalar()
    
    @hybrid_method
    def has_feedback(self, recipe_id):
        return db.session.query(Recipe).join(User, Recipe.user_id == self.id).where(Recipe.id == recipe_id).scalar()
        

class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(40))
    description: Mapped[int] = mapped_column(Text())

class Recipe(Base):
    __tablename__ = 'recipes'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text())
    time: Mapped[int] = mapped_column(Integer)
    portions: Mapped[int] = mapped_column(Integer)
    ingredients: Mapped[str] = mapped_column(Text())
    steps: Mapped[str] = mapped_column(Text())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    @hybrid_method
    def get_avg_rating(self):
        return db.session.query(func.avg(Feedback.rating)).join(Recipe, Recipe.id == Feedback.recipe_id).where(Recipe.id == self.id).scalar()
    
    @hybrid_method
    def get_feedbacks_number(self):
        return db.session.query(func.count(Feedback.id)).join(Recipe, Recipe.id == Feedback.recipe_id).where(Recipe.id == self.id).scalar()

class File(Base):
    __tablename__ = 'files'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    mime_type: Mapped[str] = mapped_column(String(50))
    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipes.id', ondelete='CASCADE'))

class Feedback(Base):
    __tablename__ = 'feedbacks'

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipes.id', ondelete='CASCADE'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    rating: Mapped[int] = mapped_column(Integer)
    feedback_text: Mapped[str] = mapped_column(Text())
    created_at: Mapped[date] = mapped_column(default=func.current_timestamp())
