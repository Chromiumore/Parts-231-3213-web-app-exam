from app.models import User, Role

class RoleRepository:
    def __init__(self, db):
        self.db = db
    
    def get_user_role(self, user_id):
        query = self.db.select(Role).join(User, User.role_id == Role.id).where(User.id == user_id)
        self.db.session.exeute(query).scalar()