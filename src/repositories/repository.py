from sqlalchemy import exc
from database import database as default_db
from entities.meal import Meal

class Repository:
    def __init__(self, db_obj=default_db):
        self.database = db_obj

    def find_all_meals(self):
        query = self.database.session.execute("SELECT name FROM meals")
        results = query.fetchall()

        if len(results) == 0:
            return results

        meals = [Meal(meal.name) for meal in results]

        return meals

        """try:
        except Exception:
            return []"""
