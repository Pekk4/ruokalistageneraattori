from db import db

class Repository:
    def __init__(self, db_obj=False):
        #self.db = db_obj
        self.db = db

    def find_all_meals(self):
        results = self.db.session.execute("SELECT name FROM meals")
        meals = results.fetchall()

        return meals
