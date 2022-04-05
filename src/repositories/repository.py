from database import database as default_db
from entities.meal import Meal

class Repository:
    def __init__(self, database=default_db):
        self.database = database

    def find_all_meals(self):
        results = self._read_from_database("SELECT name FROM meals")

        if len(results) == 0:
            return results

        meals = [Meal(meal.name) for meal in results]

        return meals

    def add_user(self, username, password):
        query = "INSERT INTO users (username, password) VALUES (:username, :password)"

        self._write(query, {"username":username, "password":password})

    def _write(self, query, items):
        try:
            self.database.session.execute(query, items)
            self.database.session.commit()
            
        except Exception:
            raise

    def _read_from_database(self, query):
        try:
            rows = self.database.session.execute(query)
            results = rows.fetchall()

            return results

        except Exception:
            raise
