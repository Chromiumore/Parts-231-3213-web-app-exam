from app.models import File, Recipe

class FileRepository:
    def __init__(self, db):
        self.db = db

    def get_recipe_files(self, recipe_id):
        query = self.db.select(File).where(File.recipe_id == recipe_id)
        return self.db.session.execute(query).scalars()
    
    def get_file_by_filename(self, filename):
        query = self.db.select(File).where(File.name == filename)
        return self.db.session.execute(query).scalar()

    def create_files(self, files):
        try:
            self.db.session.add_all(files)
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e
    
    def delete_files(self, recipe_id):
        try:
            self.db.session.query(File).where(File.recipe_id == recipe_id).delete()
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e
        return True

    