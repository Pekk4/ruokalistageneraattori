import unittest
from unittest.mock import Mock
from datetime import datetime

from entities.meal import Meal
from entities.menu import Menu
from entities.errors import InsertingError
from repositories.menu_repository import MenuRepository
from repositories.io import InputOutput


class TestMenuRepository(unittest.TestCase):
    def setUp(self):
        self.io_mock = Mock(InputOutput)
        self.repository = MenuRepository(self.io_mock)

        self.insert_query = """
            INSERT INTO menus (user_id, timestamp) VALUES (:user_id, :timestamp)
            ON CONFLICT (user_id, DATE_PART('week', timestamp), DATE_PART('year', timestamp))
            DO UPDATE SET timestamp = :timestamp RETURNING id"""
        self.select_query = """
            SELECT m.id AS menu_id, m.timestamp AS timestamp, i.id AS meal_id, i.name AS meal_name
            FROM menus m LEFT JOIN menu_meals n ON m.id = n.menu_id LEFT JOIN meals i ON
            n.meal_id = i.id WHERE m.user_id = :user_id AND DATE_PART('week', m.timestamp) =
            DATE_PART('week', NOW()) AND DATE_PART('year', m.timestamp) = DATE_PART('year', NOW())
            ORDER BY n.day_of_week"""

        meals = [Meal("Surströmming"+f"{i}", i) for i in range(7)]

        self.date = datetime.now()
        self.menu = Menu(meals, self.date)
        self.return_value = [RowMock("Surströmming"+f"{i}", i, self.date, 1) for i in range(7)]

        self.io_mock.read.return_value = self.return_value

    @staticmethod
    def get_sql_queries(query):
        old_menus_query = """
            SELECT m.id AS menu_id, m.timestamp AS timestamp, i.id AS meal_id, i.name AS meal_name
            FROM menus m LEFT JOIN menu_meals n ON m.id = n.menu_id LEFT JOIN meals i ON
            n.meal_id = i.id WHERE m.user_id = :user_id AND (DATE_PART('week', timestamp) !=
            DATE_PART('week', NOW()) OR DATE_PART('year', timestamp) != DATE_PART('year', NOW()))
            ORDER BY timestamp DESC, n.day_of_week ASC"""
        fetch_by_year_week_query = """
            SELECT m.id AS menu_id, m.timestamp AS timestamp, i.id AS meal_id, i.name AS meal_name
            FROM menus m LEFT JOIN menu_meals n ON m.id = n.menu_id LEFT JOIN meals i ON
            n.meal_id = i.id WHERE m.user_id = :user_id AND DATE_PART('week', timestamp) = :week
            AND DATE_PART('year', timestamp) = :year ORDER BY n.day_of_week"""

        if query == "old_menus":
            return old_menus_query
        if query == "year_week":
            return fetch_by_year_week_query

        return "paska"

    def test_upsert_menu_calls_write_method_correct(self):
        self.io_mock.write.return_value = Exception

        try:
            self.repository.upsert_menu(self.menu, 1)
        except Exception:
            self.io_mock.write.assert_called_with(self.insert_query, {"user_id":1, "timestamp":self.date})

    def test_upsert_menu_does_not_call_write_method_incorrect(self):
        self.io_mock.write.return_value = Exception

        try:
            self.repository.upsert_menu(self.menu, 1)
        except Exception:
            false_query = self.insert_query + ", timestamp"

            self.assertFalse(false_query in self.io_mock.write.call_args.args)
            self.assertFalse({"user_id":2, "timestamp":self.date} in self.io_mock.write.call_args.args)

    def test_upsert_menu_raises_exception_when_errors_occurred(self):
        self.io_mock.write.return_value = False

        with self.assertRaises(InsertingError) as error:
            self.repository.upsert_menu(self.menu, 1)

        self.assertEqual(str(error.exception), "An error occurred during inserting menu, aborted.")

    def test_upsert_menu_calls_submethod_correct(self):
        delete_query = "DELETE FROM menu_meals WHERE menu_id = :menu_id"
        insert_query = "INSERT INTO menu_meals (menu_id, meal_id, day_of_week) VALUES (:menu_id, :meal_id, :day)"
        meals = [{"menu_id":666, "meal_id":meal.id, "day":meal.id} for meal in self.menu.meals]

        self.io_mock.write.return_value = (666,)

        self.repository.upsert_menu(self.menu, 1)

        self.io_mock.write.assert_called_with(delete_query, {"menu_id":666})
        self.io_mock.write_many.assert_called_with(insert_query, meals)

    def test_upsert_menu_does_not_call_submethod_incorrect(self):
        false_delete_query = "DELETE FROM menu_meals WHERE id > 0"
        false_insert_query = "INSERT INTO menu_meal (menu_id, meal_id) VALUES (:menu_id, :meal_id)"

        self.io_mock.write.return_value = (666,)

        self.repository.upsert_menu(self.menu, 1)

        self.assertFalse(false_delete_query in self.io_mock.write.call_args.args)
        self.assertFalse(false_insert_query in self.io_mock.write.call_args.args)

    def test_fetch_menu_calls_read_method_correct(self):
        self.repository.fetch_current_menu(1)

        self.io_mock.read.assert_called_with(self.select_query, {"user_id":1})

    def test_fetch_menu_does_not_call_read_method_incorrect(self):
        false_query = self.select_query + " ASC"

        self.repository.fetch_current_menu(1)

        self.assertFalse(false_query in self.io_mock.read.call_args.args)

    def test_fetch_menu_returns_correct_when_no_results(self):
        self.io_mock.read.return_value = []

        return_value = self.repository.fetch_current_menu(1)

        self.assertFalse(return_value)

    def test_fetch_menu_returns_correct_objects_when_is_results(self):
        fetched_menu = self.repository.fetch_current_menu(1)

        self.assertIsInstance(fetched_menu, Menu)
        self.assertIsInstance(fetched_menu.meals[0], Meal)

    def test_fetch_menu_returns_menu_object_with_correct_details(self):
        fetched_menu = self.repository.fetch_current_menu(1)

        self.assertEqual(fetched_menu.timestamp, self.date)
        self.assertEqual(fetched_menu.db_id, self.return_value[0].menu_id)

    def test_fetch_menu_returns_menu_object_with_enough_meals_in_it(self):
        fetched_menu = self.repository.fetch_current_menu(1)

        self.assertEqual(len(fetched_menu.meals), 7)

    def test_fetch_menu_returns_menu_object_with_correct_meals_in_it(self):
        fetched_menu = self.repository.fetch_current_menu(1)

        self.assertEqual(fetched_menu.meals[0].id, self.return_value[0].meal_id)
        self.assertEqual(fetched_menu.meals[0].name, self.return_value[0].meal_name)

    def test_replace_menu_meal_calls_write_method_correct(self):
        query = """
            UPDATE menu_meals SET meal_id = :new_id WHERE menu_id = (SELECT id FROM menus WHERE
            user_id = :user_id AND DATE_PART('week', timestamp) = DATE_PART('week', NOW())) AND
            day_of_week = :day"""
        parameters = {"user_id":1, "new_id":1, "day":1}

        self.repository.replace_menu_meal(1, 1, 1)

        self.io_mock.write.assert_called_with(query, parameters)

    def test_replace_menu_meals_does_not_call_write_method_incorrect(self):
        false_query = """
            UPDATE menu_meals SET meal_id = :new_id WHERE menu_id = (SELECT id FROM menus WHERE
            user_id = :user_id AND DATE_PART('week', timestamp) = DATE_PART('week', NOW()))"""

        self.repository.replace_menu_meal(666, 666, 666)

        self.assertFalse(false_query in self.io_mock.write.call_args.args)

    def test_replace_menu_returns_correct(self):
        self.io_mock.write.return_value = True

        self.assertTrue(self.repository.replace_menu_meal(666, 13, 7))

    def test_fetch_old_menus_calls_read_method_correct_when_unlimited(self):
        query = self.get_sql_queries("old_menus")
        parameters = {"user_id":1}

        self.repository.fetch_old_menus(1)

        self.io_mock.read.assert_called_with(query, parameters)

    def test_fetch_old_menus_calls_read_method_correct_when_limited(self):
        query = self.get_sql_queries("old_menus") + " LIMIT 5"
        parameters = {"user_id":1}

        self.repository.fetch_old_menus(1, 5)

        self.io_mock.read.assert_called_with(query, parameters)

    def test_fetch_old_menus_does_not_call_read_method_incorrect(self):
        false_query = self.get_sql_queries("old_menus") + " LIMIT 5"

        self.repository.fetch_old_menus(1, 3)

        self.assertFalse(false_query in self.io_mock.read.call_args.args)

    def test_fetch_old_menus_returns_correct_when_no_results(self):
        self.io_mock.read.return_value = []

        return_value = self.repository.fetch_old_menus(1)

        self.assertIsInstance(return_value, list)
        self.assertEqual(len(return_value), 0)

    def test_fetch_old_menus_returns_correct_object_when_is_results(self):
        return_value = self.repository.fetch_old_menus(1)

        self.assertIsInstance(return_value, list)
        self.assertIsInstance(return_value[0], Menu)

    def test_fetch_old_menus_returns_menu_with_seven_meals_in_it(self):
        return_value = self.repository.fetch_old_menus(1)[0]

        self.assertIsInstance(return_value.meals, list)
        self.assertIsInstance(return_value.meals[0], Meal)

    def test_fetch_old_menus_returns_two_different_menus(self):
        another_meals = [RowMock("Lohikeitto"+f"{i}", i, self.date, 2) for i in range(8,15)]

        self.io_mock.read.return_value = self.return_value + another_meals

        return_value = self.repository.fetch_old_menus(1)

        self.assertEqual(len(return_value), 2)
        self.assertIsInstance(return_value[0], Menu)
        self.assertIsInstance(return_value[1], Menu)
        self.assertNotEqual(return_value[0], return_value[1])

    def test_fetch_old_menus_returned_menus_have_different_meals(self):
        another_meals = [RowMock("Lohikeitto"+f"{i}", i, self.date, 2) for i in range(8,15)]

        self.io_mock.read.return_value = self.return_value + another_meals

        return_value = self.repository.fetch_old_menus(1)

        self.assertFalse(Meal(another_meals[0].meal_name) in return_value[0].meals)
        self.assertFalse(Meal(self.return_value[0].meal_name) in return_value[1].meals)
        self.assertTrue(Meal(self.return_value[0].meal_name) in return_value[0].meals)
        self.assertTrue(Meal(another_meals[6].meal_name) in return_value[1].meals)

    def test_fetch_old_menus_returns_menu_with_correct_timestamp(self):
        return_value = self.repository.fetch_old_menus(1)

        self.assertEqual(return_value[0].timestamp, self.date)

    def test_fetch_old_menus_returns_menu_with_correct_menu_id(self):
        return_value = self.repository.fetch_old_menus(1)

        self.assertEqual(return_value[0].db_id, 1)

    def test_fetch_menu_by_year_and_week_calls_read_method_correct(self):
        query = self.get_sql_queries("year_week")
        parameters = {"user_id":1, "week":1, "year":1970}

        self.repository.fetch_menu_by_year_and_week(1, 1970, 1)

        self.io_mock.read.assert_called_with(query, parameters)

    def test_fetch_menu_by_year_and_week_does_not_call_read_method_incorrect(self):
        false_query = self.get_sql_queries("year_week") + " LIMIT 1"

        self.repository.fetch_menu_by_year_and_week(1, 1970, 1)

        self.assertFalse(false_query in self.io_mock.read.call_args.args)

    def test_fetch_menu_by_year_and_week_returns_correct_when_no_results(self):
        self.io_mock.read.return_value = []

        return_value = self.repository.fetch_menu_by_year_and_week(1, 1970, 1)

        self.assertIsInstance(return_value, list)
        self.assertEqual(len(return_value), 0)

    def test_fetch_menu_by_year_and_week_returns_correct_object(self):
        return_value = self.repository.fetch_menu_by_year_and_week(1, 1970, 1)

        self.assertIsInstance(return_value, Menu)
        self.assertEqual(len(return_value.meals), 7)
        self.assertIsInstance(return_value.meals[0], Meal)
        self.assertEqual(return_value.timestamp, self.date)
        self.assertEqual(return_value.db_id, 1)


class RowMock():
    def __init__(self, meal_name, meal_id, timestamp, menu_id):
        self.meal_name = meal_name
        self.meal_id = meal_id
        self.timestamp = timestamp
        self.menu_id = menu_id
