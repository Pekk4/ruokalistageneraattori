from argon2 import PasswordHasher

from services.generator import GeneratorService
from repositories.menu_repository import MenuRepository as default_menu_repository
from repositories.meal_repository import MealRepository as default_meal_repository
from repositories.user_repository import UserRepository as default_user_repository
from entities.errors import InsertingError


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

    def fetch_menu(self):
        meals = self.menu_repository.fetch_menu(1) # HUOM! user-id

        return meals

    def generate_menu(self):
        menu = self.generator.generate()

        self.menu_repository.upsert_menu(menu, 1) # HUOM! user-id

        ### TRY CATCH tännekin

    def insert_new_user(self, username, password):
        hash_value = self.password_hasher.hash(password)

        self.user_repository.add_user(username, hash_value)

    def login_user(self, username, password):
        user = self.user_repository.find_single_user(username)

        try:
            return self.password_hasher.verify(user[0].password, password)
        except Exception: # ???
            return False

    def add_meal(self, inputs_dict):
        meal = inputs_dict.pop("meal")
        ingredients = list(inputs_dict.values())

        try:
            meal_id = self.meal_repository.insert_meal(meal)
            ingredient_ids = self.meal_repository.insert_ingredients(ingredients)
            self.meal_repository.insert_meal_ingredients(meal_id, ingredient_ids)

        except InsertingError as error: # tähän jotain järkeä
            return str(error)

        return True # Necessary?

    def fetch_meals(self):
        meals = self.meal_repository.find_all_meals()

        return meals
