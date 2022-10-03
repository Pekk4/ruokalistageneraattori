from argon2 import PasswordHasher, exceptions

from services.generator import GeneratorService
from repositories.menu_repository import MenuRepository as default_menu_repository
from repositories.meal_repository import MealRepository as default_meal_repository
from repositories.user_repository import UserRepository as default_user_repository
from entities.errors import InsertingError
from utilities import DAYS


class Service:
    def __init__(
        self,
        user_repository=default_user_repository(),
        menu_repository=default_menu_repository(),
        meal_repository=default_meal_repository(),
        generator=False
    ):

        self.user_repository = user_repository
        self.menu_repository = menu_repository
        self.meal_repository = meal_repository
        self.password_hasher = PasswordHasher()
        self.generator = generator or GeneratorService(self.meal_repository)

    def fetch_menu(self, user_id):
        menu = self.menu_repository.fetch_menu(user_id)

        return menu

    def generate_menu(self, user_id):
        menu = self.generator.generate_menu(user_id)

        self.menu_repository.upsert_menu(menu, user_id)

        ### TRY CATCH tännekin

    def insert_new_user(self, username, password):
        hash_value = self.password_hasher.hash(password)

        self.user_repository.add_user(username, hash_value)

    def login_user(self, username, password):
        user = self.user_repository.find_single_user(username)

        if not user:
            return False

        try:
            self.password_hasher.verify(user[0].password, password)
        except exceptions.VerifyMismatchError:
            return False
        else:
            return (user[0].username, user[0].id)

    def add_meal(self, inputs_dict, user_id):
        meal = inputs_dict.pop("meal")
        ingredients = list(inputs_dict.values())

        try:
            meal_id = self.meal_repository.insert_meal(meal, user_id)
            ingredient_ids = self.meal_repository.insert_ingredients(ingredients, user_id)
            self.meal_repository.insert_meal_ingredients(meal_id, ingredient_ids)

        except InsertingError as error: # tähän jotain järkeä
            return str(error)

        return True # Necessary?

    def fetch_users_meals(self, user_id):
        meals = self.meal_repository.find_all_meals(user_id)

        return meals

    def generate_meal(self, user_id):
        menu = self.fetch_menu(user_id)
        meal = self.generator.generate_meal(user_id, menu)

        return meal

    def replace_meal(self, user_id, form_data):
        (day, meal_id) = form_data
        day_number = DAYS[day]

        self.menu_repository.replace_menu_meal(user_id, meal_id, day_number)
