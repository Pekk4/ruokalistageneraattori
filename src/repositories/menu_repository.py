from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from entities.ingredient import Ingredient
from entities.meal import Meal
from entities.menu import Menu
from utils.errors import InsertingError, NoResultsWarning, ReadDatabaseError
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

        try:
            menu_id = self.db_io.write(query, parameters)
        except (SQLAlchemyError, IntegrityError):
            raise InsertingError("menu")

        if not menu_id:
            raise InsertingError("menu")

        menu_id = menu_id[0]

        self._insert_menu_meals(menu_id, menu.meals)

    def _insert_menu_meals(self, menu_id: int, meals: list):
        delete_query = "DELETE FROM menu_meals WHERE menu_id = :menu_id"
        insert_query = "INSERT INTO menu_meals (menu_id, meal_id, day_of_week) VALUES (:menu_id, :meal_id, :day)"
        meals = [{"menu_id":menu_id, "meal_id":meal.db_id, "day":i} for i, meal in enumerate(meals)]

        try:
            self.db_io.write(delete_query, {"menu_id": menu_id})
            self.db_io.write_many(insert_query, meals)
        except (SQLAlchemyError, IntegrityError):
            raise InsertingError("menu")

    def fetch_current_menu(self, user_id: int):
        query = """
            SELECT m.id AS menu_id, m.timestamp AS timestamp, e.id AS meal_id, CASE WHEN e.name
            IS NULL THEN 'Ei ruokalajia' ELSE e.name END AS meal_name,
            json_agg(json_build_object('ingredient_id', i.id, 'ingredient_name', i.name, 'quantity',
            n.quantity, 'qty_unit', n.qty_unit)) AS ingredients FROM menus m LEFT JOIN menu_meals r
            ON m.id = r.menu_id LEFT JOIN meals e ON r.meal_id = e.id LEFT JOIN meal_ingredients n
            ON e.id = n.meal_id LEFT JOIN ingredients i ON n.ingredient_id = i.id WHERE
            m.user_id = :user_id AND DATE_PART('week', m.timestamp) = DATE_PART('week', NOW()) AND
            DATE_PART('year', m.timestamp) = DATE_PART('year', NOW())
            GROUP BY r.day_of_week, m.id, e.id ORDER BY r.day_of_week"""
        parameters = {"user_id": user_id}

        try:
            results = self.db_io.read(query, parameters)
        except SQLAlchemyError:
            raise ReadDatabaseError

        if not results:
            raise NoResultsWarning

        return self._build_menu_with_ingredients(results)

    def replace_menu_meal(self, user_id: int, new_id: int, day_of_week: int):
        query = """
            UPDATE menu_meals SET meal_id = :new_id WHERE menu_id = (SELECT id FROM menus WHERE
            user_id = :user_id AND DATE_PART('week', timestamp) = DATE_PART('week', NOW()) AND
            DATE_PART('year', timestamp) = DATE_PART('year', NOW())) AND
            day_of_week = :day"""
        parameters = {"user_id":user_id, "new_id":new_id, "day":day_of_week}

        try:
            return self.db_io.write(query, parameters)
        except (SQLAlchemyError, IntegrityError):
            raise InsertingError("menu")

    def fetch_old_menus(self, user_id: int, limit: int=False):
        query = """
            SELECT m.id AS menu_id, m.timestamp AS timestamp, i.id AS meal_id, CASE WHEN i.name
            IS NULL THEN 'Ei ruokalajia' ELSE i.name END AS meal_name FROM menus m LEFT JOIN 
            menu_meals n ON m.id = n.menu_id LEFT JOIN meals i ON n.meal_id = i.id WHERE 
            m.user_id = :user_id AND (DATE_PART('week', timestamp) != DATE_PART('week', NOW())
            OR DATE_PART('year', timestamp) != DATE_PART('year', NOW()))
            ORDER BY timestamp DESC, n.day_of_week ASC"""
        parameters = {"user_id":user_id}

        if limit and isinstance(limit, int):
            query = query + f" LIMIT {limit}"

        try:
            results = self.db_io.read(query, parameters)
        except SQLAlchemyError:
            raise ReadDatabaseError

        if not results:
            raise NoResultsWarning

        menus = []
        rows = []

        for result in results:
            rows.append(result)

            if len(rows) == 7:
                menus.append(self._build_menu_without_ingredients(rows.copy()))

                rows.clear()

        return menus

    def fetch_menu_by_year_and_week(self, user_id: int, year: int, week: int):
        query = """
            SELECT m.id AS menu_id, m.timestamp AS timestamp, i.id AS meal_id, CASE WHEN i.name
            IS NULL THEN 'Ei ruokalajia' ELSE i.name END AS meal_name
            FROM menus m LEFT JOIN menu_meals n ON m.id = n.menu_id LEFT JOIN meals i ON
            n.meal_id = i.id WHERE m.user_id = :user_id AND DATE_PART('week', timestamp) = :week
            AND DATE_PART('year', timestamp) = :year ORDER BY n.day_of_week"""
        parameters = {"user_id":user_id, "week":week, "year":year}

        try:
            results = self.db_io.read(query, parameters)
        except SQLAlchemyError:
            raise ReadDatabaseError

        if not results:
            raise NoResultsWarning

        return self._build_menu_without_ingredients(results)


    @staticmethod
    def _build_menu_with_ingredients(sql_rows):
        meals = []

        for row in sql_rows:
            ingredients = []

            for item in row.ingredients:
                ingredients.append(
                    Ingredient(
                        name = item["ingredient_name"],
                        qty = item["quantity"],
                        qty_unit = item["qty_unit"],
                        db_id = item["ingredient_id"]
                        )
                    )

            ingredients.sort()

            meals.append(Meal(name=row.meal_name, ingredients=ingredients.copy(), db_id=row.meal_id))

        return Menu(meals=meals, timestamp=sql_rows[0].timestamp, db_id=sql_rows[0].menu_id)

    @staticmethod
    def _build_menu_without_ingredients(sql_rows):
        meals = [Meal(name=result.meal_name, db_id=result.meal_id) for result in sql_rows]

        return Menu(meals=meals, timestamp=sql_rows[0].timestamp, db_id=sql_rows[0].menu_id)
