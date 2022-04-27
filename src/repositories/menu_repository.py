from entities.meal import Meal
from entities.menu import Menu
from repositories.io import InputOutput as default_io


class MenuRepository():
    def __init__(self, database_io=default_io()):
        self.db_io = database_io

    def upsert_menu(self, menu, user_id):
        query = """
            INSERT INTO menus (user_id, timestamp) VALUES (:user_id, :timestamp)
            ON CONFLICT (user_id, DATE_PART('week', timestamp), DATE_PART('year', timestamp))
            DO UPDATE SET timestamp = :timestamp RETURNING id"""
        parameters = {"user_id": user_id, "timestamp": menu.timestamp}

        menu_id = self.db_io.write(query, parameters)[0]

        self._insert_menu_meals(menu_id, menu.meals)

    def _insert_menu_meals(self, menu_id, meals):
        delete_query = "DELETE FROM menu_meals WHERE menu_id = :menu_id"

        self.db_io.write(delete_query, {"menu_id": menu_id})

        for meal in meals:
            query = "INSERT INTO menu_meals (menu_id, meal_id) VALUES (:menu_id, :meal_id)"
            parameters = {"menu_id": menu_id, "meal_id": meal.id}

            self.db_io.write(query, parameters)

        # Not the most efficient solution, should be improved later.

    def fetch_menu(self, user_id):
        # user_id not used anywhere yet?
        query = """
            SELECT m.id AS menu_id, m.user_id AS user_id, m.timestamp AS timestamp,
            i.id AS meal_id, i.name AS meal_name FROM menus m LEFT JOIN menu_meals n
            ON m.id = n.menu_id LEFT JOIN meals i ON n.meal_id = i.id
            WHERE m.user_id = :user_id ORDER BY n.id"""
        parameters = {"user_id": user_id}

        results = self.db_io.read(query, parameters)

        if len(results) < 1:
            return results

        meals = [Meal(result.meal_name, result.meal_id) for result in results]

        if len(meals) < 7:
            return []

        return Menu(meals, results[0].timestamp, results[0].menu_id)

    """
    def update_meals_example(self, old_menu, new_menu, user_id):
        for old_meal, new_meal in zip(old_menu.meals, new_menu.meals):
            query = \"""UPDATE menu_meals SET meal_id = :new_meal_id
                WHERE menu_id = :menu_id AND meal_id = :old_meal_id RETURNING id\"""
            parameters = {"menu_id":menu_id, "new_meal_id":new_meal.id, "old_meal_id":old_meal.id}

            self.db_io.write(query, parameters)
    """
