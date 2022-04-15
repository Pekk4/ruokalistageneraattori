from random import randint, shuffle
from datetime import datetime
from entities.menu import Menu

class GeneratorService:
    def __init__(self, repository):
        self.repository = repository

    def generate(self):
        source = self.repository.find_all_meals()
        generated_menu = []

        if len(source) < 7:
            raise NotEnoughMealsError("Not enough meals in the database")

        while len(generated_menu) < 7:
            item = source[randint(0, len(source)-1)]

            if item not in generated_menu:
                generated_menu.append(item)

        shuffle(generated_menu)

        return Menu(generated_menu, datetime.now())

class NotEnoughMealsError(Exception):
    pass
