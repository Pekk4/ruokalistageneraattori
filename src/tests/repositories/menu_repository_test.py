import unittest
from unittest.mock import patch
from datetime import datetime
from entities.meal import Meal
from entities.menu import Menu
from repositories.menu_repository import MenuRepository


class TestMenuRepository(unittest.TestCase):
    def setUp(self):
        self.repository = MenuRepository()

        self.insert_query = """
            INSERT INTO menus (user_id, timestamp) VALUES (:user_id, :timestamp)
            ON CONFLICT (user_id, DATE_PART('week', timestamp), DATE_PART('year', timestamp))
            DO UPDATE SET timestamp = :timestamp RETURNING id"""
        self.select_query = """
            SELECT m.id AS menu_id, m.user_id AS user_id, m.timestamp AS timestamp,
            i.id AS meal_id, i.name AS meal_name FROM menus m LEFT JOIN menu_meals n
            ON m.id = n.menu_id LEFT JOIN meals i ON n.meal_id = i.id
            WHERE m.user_id = :user_id ORDER BY n.id"""

        self.meals = [Meal("Surströmming", i) for i in range(7)]
        self.date = datetime.now()
        self.menu = Menu(self.meals, self.date)
        self.return_value = [RowMock("Surströmming", i, self.date, 1) for i in range(7)]

    @patch("repositories.io.InputOutput.write")
    def test_upsert_menu_calls_io_methods_correctly(self, write_mock):
        parameters = {"user_id": 1, "timestamp": self.date}

        self.repository.upsert_menu(self.menu, 1)

        write_mock.assert_any_call(self.insert_query, parameters)

    @patch("repositories.io.InputOutput.write")
    def test_upsert_menu_sub_method_calls_io_methods_correctly(self, write_mock):
        delete_query = "DELETE FROM menu_meals WHERE menu_id = :menu_id"
        meals_query = "INSERT INTO menu_meals (menu_id, meal_id) VALUES (:menu_id, :meal_id)"
        meals_parameters = {"menu_id": 666, "meal_id": 6}

        write_mock.return_value = [666]

        self.repository.upsert_menu(self.menu, 666)

        write_mock.assert_any_call(delete_query, {"menu_id": 666})
        write_mock.assert_called_with(meals_query, meals_parameters)

    @patch("repositories.io.InputOutput.write")
    def test_upsert_with_wrong_parameters_asserted_raises_assertion_error(self, write_mock):
        parameters = {"user_id": 666, "timestamp": self.date}

        self.repository.upsert_menu(self.menu, 1)

        with self.assertRaises(AssertionError):
            write_mock.assert_any_call(self.insert_query, parameters)
            write_mock.assert_called_with(self.insert_query, parameters)

    @patch("repositories.io.InputOutput.read")
    def test_fetch_menu_calls_io_methods_correctly(self, read_mock):
        read_mock.return_value = self.return_value

        self.repository.fetch_menu(1)

        read_mock.assert_called_with(self.select_query, {"user_id": 1})

    @patch("repositories.io.InputOutput.read")
    def test_fetch_menu_returns_correctly_when_no_results(self, read_mock):
        read_mock.return_value = []

        results = self.repository.fetch_menu(1)

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 0)

    @patch("repositories.io.InputOutput.read")
    def test_fetch_menu_returns_correct_object_when_results(self, read_mock):
        read_mock.return_value = self.return_value
        result = self.repository.fetch_menu(1)

        self.assertIsInstance(result, Menu)
        self.assertIsInstance(result.meals[0], Meal)
        self.assertEqual(len(result.meals), 7)
        self.assertEqual(result.timestamp, self.date)
        self.assertEqual(result.db_id, self.return_value[0].menu_id)
        self.assertEqual(result.meals[0].id, self.return_value[0].meal_id)
        self.assertEqual(result.meals[0].name, self.return_value[0].meal_name)

    @patch("repositories.io.InputOutput.read")
    def test_fetch_menu_returns_correctly_when_not_enough_meals(self, read_mock):
        self.return_value.pop()
        read_mock.return_value = self.return_value

        self.assertIsInstance(self.repository.fetch_menu(1), list)

    @patch("repositories.io.InputOutput.read")
    def test_fetch_menu_raises_assertion_error_with_incorrect_parameters_asserted(self, read_mock):
        self.repository.fetch_menu(1)

        with self.assertRaises(AssertionError):
            read_mock.assert_any_call(self.select_query, {"user_id": 666})
            read_mock.assert_called_with(self.select_query, {"user_id": 666})


class RowMock():
    def __init__(self, meal_name, meal_id, timestamp, menu_id):
        self.meal_name = meal_name
        self.meal_id = meal_id
        self.timestamp = timestamp
        self.menu_id = menu_id
