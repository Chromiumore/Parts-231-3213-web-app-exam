from app.models import Feedback, Recipe

class FeedbackRepository:
    def __init__(self, db):
        self.db = db

    def get(self, id):
        query = self.db.select(Feedback).where(Feedback.id == id)
        return self.db.session.execute(query).scalar()
    
    def get_by_recipe(self, recipe_id):
        query = self.db.select(Feedback).join(Recipe, Recipe.id == Feedback.recipe_id).where(Recipe.id == recipe_id)
        return self.db.session.execute(query).scalars()
    
    def create(self, feedback):
        try:
            self.db.session.add(feedback)
            self.db.session.commit()
            self.db.session.refresh(feedback)
        except Exception as e:
            self.db.session.rollback()
            raise e
        return feedback
    
    def update(self, id, feedback):
        try:
            self.db.session.query(Feedback).where(Feedback.id == id).update({
                Feedback.feedback_text: feedback.feedback_text,
                Feedback.rating: feedback.rating
            })
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e
        return self.db.session.query(Feedback).where(Feedback.id == id).scalar()
    
    def delete(self, id):
        try:
            self.db.session.query(Feedback).where(Feedback.id == id).delete()
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e
        return True