import unittest
from unittest.mock import patch
from datetime import datetime
from entities.meal import Meal
from entities.menu import Menu
from repositories.menu_repository import MenuRepository

class TestMenuRepository(unittest.TestCase):

    def setUp(self):
        self.repository = MenuRepository(None)

    @patch("repositories.base_repository.BaseRepository.write_items")
    def test_insert_menu_calls_super_object_correctly(self, patched_mock):
        date = datetime.now()
        query = "INSERT INTO menus (meal_ids, user_id, date) VALUES (:meal_ids, :user_id, :date)"
        parameters = {"meal_ids":list(range(7)), "user_id":1, "date":date}
        meals = [Meal("Surströmming", i) for i in range(7)]

        self.repository.insert_menu(Menu(meals, date))

        patched_mock.assert_called_with(query, parameters)

    @patch("repositories.base_repository.BaseRepository.read_items")
    def test_fetch_menu_calls_super_object_correctly(self, patched_mock):
        patched_mock.return_value = []

        self.repository.fetch_menu()

        patched_mock.assert_called()
