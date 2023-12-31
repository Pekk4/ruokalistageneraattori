from datetime import datetime

from entities.menu import Menu
from services.generator import GeneratorService
from repositories.menu_repository import MenuRepository as default_repository
from utils.utilities import MESSAGES, validate_week_number, validate_year
from utils.errors import InsertingError, NotEnoughMealsError, ReadDatabaseError, NoResultsWarning


class MenuService:
    def __init__(self, repository=default_repository(), generator=GeneratorService()):
        self.repository = repository
        self.generator = generator

    def fetch_menu(self, user_id):
        try:
            menu = self.repository.fetch_current_menu(user_id)
        except NoResultsWarning:
            return []
        except ReadDatabaseError:
            return MESSAGES["common_error"]

        return menu

    def generate_menu(self, user_id):
        try:
            menu = self.generator.generate_menu(user_id)
            self.repository.upsert_menu(menu, user_id)
        except (NotEnoughMealsError, NoResultsWarning):
            return MESSAGES["not_enough"]
        except (InsertingError, ReadDatabaseError):
            return MESSAGES["common_error"]

        return True

    def generate_meal(self, user_id):
        try:
            menu = self.repository.fetch_current_menu(user_id)
            meal = self.generator.generate_meal(user_id, menu)
        except (NotEnoughMealsError, NoResultsWarning):
            return MESSAGES["not_enough"]
        except (ValueError, ReadDatabaseError):
            return MESSAGES["common_error"]

        return meal

    def replace_meal(self, user_id, form_data):
        try:
            (day, meal_id) = form_data
            day = 0 if int(day) > 6 else day

            self.repository.replace_menu_meal(user_id, meal_id, day)
        except (ValueError, TypeError, InsertingError):
            return MESSAGES["common_error"]

        return True

    def fetch_old_menus(self, user_id: int, limit_rows: int=False):
        try:
            menus = self.repository.fetch_old_menus(user_id, limit_rows)
        except NoResultsWarning:
            return []
        except ReadDatabaseError:
            return MESSAGES["common_error"]

        return menus

    def fetch_menu_by_timestamp(self, user_id: int, week_number: int, year: int):
        try:
            week_number = int(week_number)
            year = int(year)

            validate_week_number(week_number)
            validate_year(year)

            menu = self.repository.fetch_menu_by_year_and_week(user_id, year, week_number)

        except (TypeError, ValueError, ReadDatabaseError, NoResultsWarning):
            return MESSAGES["common_error"]

        return menu

    def replace_current_menu_with(self, user_id: int , week_number: int, year: int):
        menu = self.fetch_menu_by_timestamp(user_id, week_number, year)

        if isinstance(menu, Menu):
            try:
                menu.timestamp = datetime.now()
                self.repository.upsert_menu(menu, user_id)
            except InsertingError:
                return MESSAGES["common_error"]
            else:
                return True

        return MESSAGES["common_error"]

    def fetch_menus_ingredients(self, user_id: int):
        menu = self.fetch_menu(user_id)

        if isinstance(menu, Menu):
            ingredients = [ingredient for meal in menu.meals for ingredient in meal.ingredients]

            return sorted(set(ingredients))

        return menu
