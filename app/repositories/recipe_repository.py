from app.models import Recipe

class RecipeRepository:
    def __init__(self, db):
        self.db = db

    def all(self):
        query = self.db.select(Recipe).order_by(Recipe.id)
        return self.db.session.execute(query).scalars()
    
    def get(self, id):
        query = self.db.select(Recipe).where(Recipe.id == id)
        return self.db.session.execute(query).scalar()
    
    def create(self, recipe):
        try:
            self.db.session.add(recipe)
            self.db.session.commit()
            self.db.session.refresh(recipe)
        except Exception as e:
            self.db.session.rollback()
            raise e
        return recipe
    
    def update(self, id, recipe):
        try:
            result = self.db.session.query(Recipe).where(Recipe.id == id).update({
                Recipe.name: recipe.name,
                Recipe.description: recipe.description,
                Recipe.time: recipe.time,
                Recipe.portions: recipe.portions,
                Recipe.ingredients: recipe.ingredients
            })
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e
        return self.db.session.query(Recipe).where(Recipe.id == id).scalar()
    
    def delete(self, id):
        try:
            self.db.session.query(Recipe).where(Recipe.id == id).delete()
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e
        return True