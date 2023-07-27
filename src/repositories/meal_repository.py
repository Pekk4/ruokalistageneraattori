from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from repositories.io import InputOutput as default_io
from entities.meal import Meal
from entities.ingredient import Ingredient
from utils.errors import InsertingError, MealExistsWarning, ReadDatabaseError, NoResultsWarning


class MealRepository():
    def __init__(self, database_io=default_io()):
        self.db_io = database_io

    def find_all_meals(self, user_id):
        query = """
            SELECT m.id AS meal_id, m.name AS meal_name, json_agg(json_build_object('ingredient_id',
            i.id, 'ingredient_name', i.name, 'quantity', n.quantity, 'qty_unit', n.qty_unit))
            AS ingredients FROM meals m LEFT JOIN meal_ingredients n ON m.id = n.meal_id
            LEFT JOIN ingredients i ON n.ingredient_id = i.id WHERE m.user_id = :user_id GROUP BY m.id;"""

        parameters = {"user_id":user_id}

        try:
            results = self.db_io.read(query, parameters)
        except SQLAlchemyError as original_error:
            raise ReadDatabaseError from original_error

        if not results:
            raise NoResultsWarning("No results from database.")

        return self._build_meals(results)

    def insert_meal(self, meal, user_id):
        query = "INSERT INTO meals (name, user_id) VALUES (:meal, :user_id) RETURNING id"
        parameters = {"meal":meal.name, "user_id":user_id}

        try:
            database_id = self.db_io.write(query, parameters)
        except IntegrityError as original_error:
            raise MealExistsWarning("Such meal already exists.") from original_error
        except SQLAlchemyError as original_error:
            raise InsertingError("meal") from original_error

        meal.db_id, = database_id

        return meal

    def insert_ingredients(self, meal, user_id):
        query = """
            INSERT INTO ingredients (name, user_id) VALUES (:ingredient, :user_id) ON CONFLICT
            (name, user_id) DO UPDATE SET user_id = :user_id RETURNING id"""
        parameters = [{"ingredient":ingredient.name, "user_id":user_id} for ingredient in meal.ingredients]

        try:
            database_ids = self.db_io.write_many(query, parameters)
        except SQLAlchemyError as original_error:
            raise InsertingError("ingredient") from original_error

        for (db_id,), ingredient in zip(database_ids, meal.ingredients):
            ingredient.db_id = db_id

        return meal

    def insert_meal_ingredients(self, meal, user_id):
        delete_query = "DELETE FROM meal_ingredients WHERE meal_id = :meal_id"
        insert_query = """
            INSERT INTO meal_ingredients (meal_id, ingredient_id, quantity, qty_unit)
            VALUES (:meal_id, :ingredient_id, :quantity, :qty_unit) ON CONFLICT (meal_id,
            ingredient_id) DO UPDATE SET quantity = :quantity, qty_unit = :qty_unit"""
        parameters = []

        for ingredient in meal.ingredients:
            parameters.append({
                "user_id": user_id,
                "meal_id": meal.db_id,
                "ingredient_id": ingredient.db_id,
                "quantity": ingredient.qty,
                "qty_unit": ingredient.qty_unit
                }
            )

        try:
            self.db_io.write(delete_query, parameters[0])
            self.db_io.write_many(insert_query, parameters)
        except SQLAlchemyError as original_error:
            raise InsertingError("meal's ingredients") from original_error

    def find_all_ingredients(self, user_id):
        query = "SELECT id, name FROM ingredients WHERE user_id = :user_id ORDER BY name"
        parameters = {"user_id":user_id}

        try:
            results = self.db_io.read(query, parameters)
        except SQLAlchemyError as original_error:
            raise ReadDatabaseError from original_error

        if not results:
            raise NoResultsWarning("No results from database.")

        ingredients = [Ingredient(ingredient.name, ingredient.id) for ingredient in results]

        return ingredients

    def find_single_meal(self, user_id, meal_id=None, meal_name=None):
        query = """
            SELECT m.id AS meal_id, m.name AS meal_name, i.id AS ingredient_id, i.name AS
            ingredient_name, n.quantity AS quantity, n.qty_unit AS qty_unit FROM meals m
            LEFT JOIN meal_ingredients n ON n.meal_id = m.id LEFT JOIN ingredients i
            ON n.ingredient_id = i.id WHERE m.user_id = :user_id AND """
        parameters = {"user_id":user_id, "meal_id":meal_id, "meal_name":meal_name}

        if not meal_id and not meal_name:
            raise ValueError("Meal id or name needed for query.")
        if meal_id:
            query += "m.id = :meal_id"
        elif meal_name:
            query += "m.name = :meal_name"

        try:
            results = self.db_io.read(query, parameters)
        except SQLAlchemyError as original_error:
            raise ReadDatabaseError from original_error

        if not results:
            raise NoResultsWarning("No results from database.")

        ingredients = sorted([self._build_ingredient(result) for result in results])

        return Meal(results[0].meal_name, ingredients, results[0].meal_id)

    def update_meal(self, meal, user_id):
        query = """
            INSERT INTO meals (name, user_id) VALUES (:meal, :user_id) ON CONFLICT
            (name, user_id) DO UPDATE SET user_id = :user_id RETURNING id"""
        parameters = {"meal":meal.name, "user_id":user_id}

        try:
            database_id = self.db_io.write(query, parameters)
        except SQLAlchemyError as original_error:
            raise InsertingError("meal") from original_error

        meal.db_id, = database_id

        return meal

    def delete_meal(self, user_id, meal_id):
        query = "DELETE FROM meals WHERE id = :meal_id AND user_id = :user_id"
        parameters = {"user_id":user_id, "meal_id":meal_id}

        try:
            self.db_io.write(query, parameters)
        except SQLAlchemyError as original_error:
            raise InsertingError("Nönnönnöö") from original_error

    def _build_meals(self, meals_data):
        meals = []

        for row in meals_data:
            ingredients = []

            for item in row.ingredients:
                self._build_ingredient(item)

            ingredients.sort()

            meals.append(Meal(row.meal_name, ingredients.copy(), row.meal_id))

        return meals


    @staticmethod
    def _build_ingredient(result_row):
        return Ingredient(
            result_row["ingredient_name"],
            result_row["quantity"],
            result_row["qty_unit"],
            result_row["ingredient_id"]
        )
