from database import database as default_db
from repositories.base_repository import BaseRepository
from entities.meal import Meal
from entities.menu import Menu


class MenuRepository(BaseRepository):

    def __init__(self, database=default_db):
        super().__init__(database)

    def insert_menu(self, menu):
        query = "INSERT INTO menus (meal_ids, user_id, date) VALUES (:meal_ids, :user_id, :date)"
        meal_ids = [meal.id for meal in menu.meals]
        parameters = {"meal_ids":meal_ids, "user_id":1, "date":menu.date}

        super().write_items(query, parameters)

    def fetch_menu(self):
        query = "SELECT b.id, (SELECT ARRAY(SELECT CONCAT(m.id, ';', m.name) FROM meals m " \
                "JOIN UNNEST((SELECT a.meal_ids FROM menus a WHERE a.id = b.id)) WITH " \
                "ORDINALITY o(id, ord) USING (id) ORDER BY o.ord) AS meals), " \
                "b.user_id, b.date FROM menus b"

        results = super().read_items(query)

        if not results:
            return False # Temp

        results = results[-1] # Vain viimeinen lista 4 POCcing
        meals = []

        for meal in results.meals:
            id, name = meal.split(";")

            meals.append(Meal(name, id))

        return Menu(meals, results.date, results.id)
