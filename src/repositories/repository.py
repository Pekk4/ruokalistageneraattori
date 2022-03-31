from database import database as default_db

class Repository:
    def __init__(self, db_obj=default_db):
        self.database = db_obj

    def find_all_meals(self):
        results = self.database.session.execute("SELECT name FROM meals")
        meals = results.fetchall()

        return meals
