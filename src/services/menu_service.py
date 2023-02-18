from datetime import datetime

from services.generator import GeneratorService
from repositories.menu_repository import MenuRepository as default_repository
from utils.errors import InsertingError, NotEnoughMealsError, ReadDatabaseError, NoResultsWarning
from entities.menu import Menu
from utilities import MESSAGES, validate_week_number, validate_year


class MenuService:
    def __init__(self, repository=default_repository(), generator=GeneratorService()):
        self.repository = repository
        self.generator = generator
        self.week_day_indexes = list(range(7))

    def fetch_menu(self, user_id):
        try:
            menu = self.repository.fetch_current_menu(user_id)

            if isinstance(menu, Menu):
                menu = zip(menu.meals, self.week_day_indexes)
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

            if isinstance(menu, Menu):
                menu.meals = zip(menu.meals, self.week_day_indexes)
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
