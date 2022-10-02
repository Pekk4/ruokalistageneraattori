from random import randint, shuffle
from datetime import datetime

from entities.menu import Menu
from entities.errors import NotEnoughMealsError


class GeneratorService:
    def __init__(self, repository):
        self.repository = repository

    def generate_menu(self, user_id):
        generated_menu = []
        meals = self.repository.find_all_meals(user_id)

        if len(meals) < 7:
            raise NotEnoughMealsError("Not enough meals in the database")

        while len(generated_menu) < 7:
            item = meals[randint(0, len(meals)-1)]

            if item not in generated_menu:
                generated_menu.append(item)

        shuffle(generated_menu)

        return Menu(generated_menu, datetime.now())

    def generate_meal(self, user_id, menu):
        meals = self.repository.find_all_meals(user_id)

        if len(meals) <= 7:
            raise NotEnoughMealsError("Not enough meals in the database")

        while True:
            item = meals[randint(0, len(meals)-1)]

            if item not in menu.meals:
                return item
