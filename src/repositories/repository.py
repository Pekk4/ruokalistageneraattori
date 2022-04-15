from database import database as default_db
from repositories.base_repository import BaseRepository
from entities.meal import Meal


class Repository(BaseRepository):

    def __init__(self, database=default_db):
        super().__init__(database)

    def find_all_meals(self):
        results = super().read_items("SELECT name, id FROM meals")

        if len(results) == 0:
            return results

        meals = [Meal(meal.name, meal.id) for meal in results]

        return meals

    def add_user(self, username, password):
        query = "INSERT INTO users (username, password) VALUES (:username, :password)"
        parameters = {"username":username, "password":password}

        super().write_items(query, parameters)

    def find_single_user(self, username):
        query = "SELECT username, password FROM users WHERE username=:username"
        parameters = {"username":username}

        return super().read_items(query, parameters)
