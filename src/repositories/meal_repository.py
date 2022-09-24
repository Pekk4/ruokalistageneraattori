from repositories.io import InputOutput as default_io
from entities.meal import Meal
from entities.errors import InsertingError


class MealRepository():
    def __init__(self, database_io=default_io()):
        self.db_io = database_io

    def find_all_meals(self, user_id):
        query = "SELECT id, name FROM meals WHERE user_id = :user_id"
        parameters = {"user_id":user_id}

        results = self.db_io.read(query, parameters)

        if len(results) == 0:
            return results

        meals = [Meal(meal.name, meal.id) for meal in results]

        return meals

    def insert_meal(self, meal, user_id):
        query = "INSERT INTO meals (name, user_id) VALUES (:meal, :user_id) RETURNING id"
        parameters = {"meal":meal, "user_id":user_id}

        database_id = self.db_io.write(query, parameters)

        if not database_id:
            raise InsertingError("meal")

        database_id, = database_id

        return database_id

    def insert_ingredients(self, ingredients, user_id):
        query = "INSERT INTO ingredients (name, user_id) VALUES (:ingredient, :user_id) RETURNING id"
        parameters = [{"ingredient":ingredient, "user_id":user_id} for ingredient in ingredients]

        database_ids = self.db_io.write_many(query, parameters)

        if not database_ids:
            raise InsertingError("ingredient")

        return database_ids

    def insert_meal_ingredients(self, meal_id, ingredient_ids):
        query = "INSERT INTO meal_ingredients (meal_id, ingredient_id) VALUES (:meal_id, :ingredient_id)"
        parameters = [{"meal_id":meal_id, "ingredient_id":db_id} for db_id, in ingredient_ids]

        return_value = self.db_io.write_many(query, parameters)

        if not return_value:
            raise InsertingError("meal's ingredients")

        return True # Necessary?
