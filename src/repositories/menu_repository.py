from entities.meal import Meal
from entities.menu import Menu
from entities.errors import InsertingError
from repositories.io import InputOutput as default_io


class MenuRepository():
    def __init__(self, database_io=default_io()):
        self.db_io = database_io

    def upsert_menu(self, menu: Menu, user_id: int):
        query = """
            INSERT INTO menus (user_id, timestamp) VALUES (:user_id, :timestamp)
            ON CONFLICT (user_id, DATE_PART('week', timestamp), DATE_PART('year', timestamp))
            DO UPDATE SET timestamp = :timestamp RETURNING id"""
        parameters = {"user_id": user_id, "timestamp": menu.timestamp}

        menu_id = self.db_io.write(query, parameters)

        if not menu_id:
            raise InsertingError("menu")

        menu_id = menu_id[0]

        self._insert_menu_meals(menu_id, menu.meals)

    def _insert_menu_meals(self, menu_id: int, meals: list):
        delete_query = "DELETE FROM menu_meals WHERE menu_id = :menu_id"
        insert_query = "INSERT INTO menu_meals (menu_id, meal_id, day_of_week) VALUES (:menu_id, :meal_id, :day)"
        meals = [{"menu_id":menu_id, "meal_id":meal.id, "day":i} for i, meal in enumerate(meals)]

        self.db_io.write(delete_query, {"menu_id": menu_id})
        self.db_io.write_many(insert_query, meals)

        # Not the most efficient solution, should be improved later.

    def fetch_current_menu(self, user_id: int):
        query = """
            SELECT m.id AS menu_id, m.timestamp AS timestamp, i.id AS meal_id, i.name AS meal_name
            FROM menus m LEFT JOIN menu_meals n ON m.id = n.menu_id LEFT JOIN meals i ON
            n.meal_id = i.id WHERE m.user_id = :user_id AND DATE_PART('week', m.timestamp) =
            DATE_PART('week', NOW()) AND DATE_PART('year', m.timestamp) = DATE_PART('year', NOW())
            ORDER BY n.day_of_week"""
        parameters = {"user_id": user_id}

        results = self.db_io.read(query, parameters)

        if len(results) < 7:
            return results

        return self._build_menu(results)

    def replace_menu_meal(self, user_id: int, new_id: int, day_of_week: int):
        query = """
            UPDATE menu_meals SET meal_id = :new_id WHERE menu_id = (SELECT id FROM menus WHERE
            user_id = :user_id AND DATE_PART('week', timestamp) = DATE_PART('week', NOW())) AND
            day_of_week = :day"""
        parameters = {"user_id":user_id, "new_id":new_id, "day":day_of_week}

        return self.db_io.write(query, parameters)

    def fetch_old_menus(self, user_id: int, limit: int=False):
        query = """
            SELECT m.id AS menu_id, m.timestamp AS timestamp, i.id AS meal_id, i.name AS meal_name
            FROM menus m LEFT JOIN menu_meals n ON m.id = n.menu_id LEFT JOIN meals i ON
            n.meal_id = i.id WHERE m.user_id = :user_id AND (DATE_PART('week', timestamp) !=
            DATE_PART('week', NOW()) OR DATE_PART('year', timestamp) != DATE_PART('year', NOW()))
            ORDER BY timestamp DESC, n.day_of_week ASC"""
        parameters = {"user_id":user_id}

        if limit and isinstance(limit, int):
            query = query + f" LIMIT {limit}"

        results = self.db_io.read(query, parameters)

        if len(results) < 7:
            return results

        menus = []
        rows = []

        for result in results:
            rows.append(result)

            if len(rows) == 7:
                menus.append(self._build_menu(rows.copy()))

                rows.clear()

        return menus

    def fetch_menu_by_year_and_week(self, user_id: int, year: int, week: int):
        query = """
            SELECT m.id AS menu_id, m.timestamp AS timestamp, i.id AS meal_id, i.name AS meal_name
            FROM menus m LEFT JOIN menu_meals n ON m.id = n.menu_id LEFT JOIN meals i ON
            n.meal_id = i.id WHERE m.user_id = :user_id AND DATE_PART('week', timestamp) = :week
            AND DATE_PART('year', timestamp) = :year ORDER BY n.day_of_week"""
        parameters = {"user_id":user_id, "week":week, "year":year}

        results = self.db_io.read(query, parameters)

        if len(results) < 7:
            return results

        return self._build_menu(results)

    @staticmethod
    def _build_menu(sql_rows):
        meals = [Meal(result.meal_name, result.meal_id) for result in sql_rows]

        return Menu(meals, sql_rows[0].timestamp, sql_rows[0].menu_id)
