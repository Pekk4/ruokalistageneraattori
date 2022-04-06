from repositories.io import InputOutput as default_io
from entities.meal import Meal

class Repository:
    def __init__(self, input_output=default_io()):
        self.i_o = input_output

    def find_all_meals(self):
        results = self.i_o.read("SELECT name FROM meals")

        if len(results) == 0:
            return results

        meals = [Meal(meal.name) for meal in results]

        return meals

    def add_user(self, username, password):
        query = "INSERT INTO users (username, password) VALUES (:username, :password)"

        self.i_o.write(query, {"username":username, "password":password})

    def find_single_user(self, username):
        query = "SELECT username, password FROM users WHERE username=:username"

        result = self.i_o.read(query, {"username":username})

        return result
