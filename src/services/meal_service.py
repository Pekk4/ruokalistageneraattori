from entities.ingredient import Ingredient
from entities.meal import Meal
from repositories.meal_repository import MealRepository as default_repository
from utils.errors import (InsertingError, InvalidInputError, MealExistsWarning, NoResultsWarning,
    ReadDatabaseError)
from utilities import MESSAGES

class MealService:
    def __init__(self, repository=default_repository()):
        self.repository = repository

    def fetch_user_meals(self, user_id):
        try:
            meals = self.repository.find_all_meals(user_id)
        except NoResultsWarning:
            return MESSAGES["no_meals"]
        except ReadDatabaseError:
            return MESSAGES["common_error"]

        return meals

    def fetch_user_ingredients(self, user_id):
        try:
            ingredients = self.repository.find_all_ingredients(user_id)
        except (NoResultsWarning, ReadDatabaseError):
            return []

        return ingredients

    def fetch_single_meal(self, user_id: int, meal_id: int):
        try:
            meal = self.repository.find_single_meal(user_id, meal_id=meal_id)
        except NoResultsWarning:
            return MESSAGES["no_meals"]
        except (ValueError, ReadDatabaseError):
            return MESSAGES["common_error"]

        return meal

    def add_meal(self, user_id, meal_data):
        try:
            meal = self._prepare_meal(meal_data)
            meal = self.repository.insert_meal(meal, user_id)
            meal = self.repository.insert_ingredients(meal, user_id)

            self.repository.insert_meal_ingredients(meal, user_id)
        except (InsertingError, KeyError):
            return MESSAGES["common_error"]
        except InvalidInputError:
            return MESSAGES["input_error"]
        except MealExistsWarning:
            return MESSAGES["meal_exists"]

        return True

    def update_meal(self, user_id, input_data, meal_id=None, meal_name=None):
        if not meal_id and not meal_name:
            return MESSAGES["common_error"]

        try:
            new_meal = self._prepare_meal(input_data)

            if meal_id:
                existing_meal = self.repository.find_single_meal(user_id, meal_id=meal_id)
            if meal_name:
                existing_meal = self.repository.find_single_meal(user_id, meal_name=meal_name)
        except InvalidInputError:
            return MESSAGES["input_error"]
        except (KeyError, ReadDatabaseError, NoResultsWarning):
            return MESSAGES["common_error"]

        if new_meal != existing_meal:
            try:
                meal_to_process = self.repository.update_meal(new_meal, user_id)
                meal_to_process = self.repository.insert_ingredients(meal_to_process, user_id)

                self.repository.insert_meal_ingredients(meal_to_process, user_id)
            except InsertingError:
                return MESSAGES["common_error"]

        return True

    def delete_meal(self, user_id, meal_id, meal_data):
        try:
            meal_name = meal_data["meal_name"]
            meal_from_db = self.repository.find_single_meal(user_id, meal_name=meal_name)

            if int(meal_id) == meal_from_db.db_id:
                self.repository.delete_meal(user_id, meal_id)
        except (KeyError, ReadDatabaseError, InsertingError, NoResultsWarning):
            return MESSAGES["common_error"]

    def _prepare_meal(self, meal_data):
        try:
            self._check_inputs(meal_data)

            meal = self._build_meal_from_json(meal_data)
        except (InvalidInputError, KeyError):
            raise

        return meal


    @staticmethod
    def _check_inputs(input_data: dict):
        meal_name = input_data["meal_name"]
        ingredient_name = input_data["ingredients"][0]["ingredient_name"]
        
        if len(meal_name.split()) == 0 or len(ingredient_name.split()) == 0:
            raise InvalidInputError

    @staticmethod
    def _build_meal_from_json(meal_data: dict):
        meal_name = meal_data["meal_name"].strip().capitalize()
        meal = Meal(meal_name)
        ingredients = []

        for data_item in meal_data["ingredients"]:
            ingredients.append(
                Ingredient(
                    data_item["ingredient_name"].strip().capitalize(),
                    str(data_item["qty"]).strip() if data_item["qty"] != "" else None,
                    data_item["unit"].strip() if data_item["unit"] != "" else None
                )
            )

        meal.ingredients = ingredients
        
        return meal
