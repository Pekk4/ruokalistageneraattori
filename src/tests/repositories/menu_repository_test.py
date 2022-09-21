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
            SELECT m.id AS menu_id, m.user_id AS user_id, m.timestamp AS timestamp,
            i.id AS meal_id, i.name AS meal_name FROM menus m LEFT JOIN menu_meals n
            ON m.id = n.menu_id LEFT JOIN meals i ON n.meal_id = i.id
            WHERE m.user_id = :user_id AND DATE_PART('week', timestamp) =
            DATE_PART('week', NOW()) ORDER BY n.id"""

        meals = [Meal("Surströmming", i) for i in range(7)]

        self.date = datetime.now()
        self.menu = Menu(meals, self.date)
        self.return_value = [RowMock("Surströmming", i, self.date, 1) for i in range(7)]

        self.io_mock.read.return_value = self.return_value

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
        insert_query = "INSERT INTO menu_meals (menu_id, meal_id) VALUES (:menu_id, :meal_id)"
        meals = [{"menu_id":666, "meal_id":meal.id} for meal in self.menu.meals]

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
        self.repository.fetch_menu(1)

        self.io_mock.read.assert_called_with(self.select_query, {"user_id":1})

    def test_fetch_menu_does_not_call_read_method_incorrect(self):
        false_query = self.select_query + " ASC"

        self.repository.fetch_menu(1)

        self.assertFalse(false_query in self.io_mock.read.call_args.args)

    def test_fetch_menu_returns_correct_when_no_results(self):
        self.io_mock.read.return_value = []

        return_value = self.repository.fetch_menu(1)

        self.assertFalse(return_value)

    def test_fetch_menu_returns_correct_objects_when_is_results(self):
        fetched_menu = self.repository.fetch_menu(1)

        self.assertIsInstance(fetched_menu, Menu)
        self.assertIsInstance(fetched_menu.meals[0], Meal)

    def test_fetch_menu_returns_menu_object_with_correct_details(self):
        fetched_menu = self.repository.fetch_menu(1)

        self.assertEqual(fetched_menu.timestamp, self.date)
        self.assertEqual(fetched_menu.db_id, self.return_value[0].menu_id)

    def test_fetch_menu_returns_menu_object_with_enough_meals_in_it(self):
        fetched_menu = self.repository.fetch_menu(1)

        self.assertEqual(len(fetched_menu.meals), 7)

    def test_fetch_menu_returns_menu_object_with_correct_meals_in_it(self):
        fetched_menu = self.repository.fetch_menu(1)

        self.assertEqual(fetched_menu.meals[0].id, self.return_value[0].meal_id)
        self.assertEqual(fetched_menu.meals[0].name, self.return_value[0].meal_name)


class RowMock():
    def __init__(self, meal_name, meal_id, timestamp, menu_id):
        self.meal_name = meal_name
        self.meal_id = meal_id
        self.timestamp = timestamp
        self.menu_id = menu_id
