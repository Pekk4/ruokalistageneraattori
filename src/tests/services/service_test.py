import unittest
from unittest.mock import Mock
from entities.meal import Meal
from entities.menu import Menu
from services.service import Service

class TestService(unittest.TestCase):

    def setUp(self):
        self.repository_mock = Mock()
        self.menu_repository_mock = Mock()
        self.generator_mock = Mock()

        self.test_menu = Menu(list(range(7)), "0")

        self.menu_repository_mock.fetch_menu.return_value = self.test_menu

        self.service = Service(
            self.repository_mock, self.menu_repository_mock, self.generator_mock)

    def test_fetch_menu_calls_repository_methods(self):
        self.service.fetch_menu()

        self.menu_repository_mock.fetch_menu.assert_called()

    def test_fetch_menu_returns_correct_object(self):
        menu = self.service.fetch_menu()

        self.assertIsInstance(menu, Menu)
        self.assertEqual(len(menu.meals), 7)
        self.assertEqual(menu.date, "0")

    def test_insert_new_user_calls_repository_methods(self):
        self.service.insert_new_user("Paavo", "Pesusieni")

        self.repository_mock.add_user.assert_called()
        self.assertTrue("Paavo" in self.repository_mock.add_user.call_args[0])

    def test_insert_new_user_throws_exception_without_arguments(self):
        with self.assertRaises(TypeError):
            self.service.insert_new_user() # pylint: disable=E1120

    def test_login_user_calls_repository_methods(self):
        self.service.login_user("Paavo", "Pesusieni")

        self.repository_mock.find_single_user.has_called_with("Paavo")

    def test_login_user_returns_false_when_no_results(self):
        self.assertFalse(self.service.login_user("Hölkyn", "Kölkyn"))

    def test_login_user_throws_exception_without_arguments(self):
        with self.assertRaises(TypeError):
            self.service.login_user() # pylint: disable=E1120"""

    # Hash täytyy testailla vielä

    def test_generate_menu_calls_generator_methods(self):
        self.service.generate_menu()

        self.generator_mock.generate.assert_called()

    def test_generate_menu_calls_repository_methods(self):
        self.generator_mock.generate.return_value = self.test_menu
        self.service.generate_menu()

        self.menu_repository_mock.insert_menu.assert_called_with(self.test_menu)

    def test_add_meal_calls_repository_methods(self):
        self.service.add_meal("Surströmming")

        self.repository_mock.insert_meal.assert_called_with("Surströmming")
