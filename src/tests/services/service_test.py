import unittest
from unittest.mock import Mock
from entities.meal import Meal
from services.service import Service

class TestService(unittest.TestCase):

    def setUp(self):
        self.repository_mock = Mock()
        self.service = Service(self.repository_mock)

    def test_provide_meals_calls_repository_methods(self):
        self.service.provide_meals()

        self.repository_mock.find_all_meals.assert_called()

    def test_provide_meals_returns_correct_object(self):
        meals = [Meal("Surströmming"), Meal("Pepparkakor")]
        self.repository_mock.find_all_meals.return_value = meals

        value = self.service.provide_meals()

        self.assertEqual(len(value), 2)
        self.assertIsInstance(value[0], Meal)

    def test_insert_new_user_calls_repository_methods(self):        
        self.service.insert_new_user("Paavo", "Pesusieni")

        self.repository_mock.add_user.assert_called()
        self.assertTrue("Paavo" in self.repository_mock.add_user.call_args[0])

    def test_insert_new_user_throws_exception_without_arguments(self):
        with self.assertRaises(TypeError):
            self.service.insert_new_user()

    def test_login_user_calls_repository_methods(self):
        self.service.login_user("Paavo", "Pesusieni")

        self.repository_mock.find_single_user.has_called_with("Paavo")

    def test_login_user_returns_False_when_no_results(self):
        self.assertFalse(self.service.login_user("Hölkyn", "Kölkyn"))

    def test_login_user_throws_exception_without_arguments(self):
        with self.assertRaises(TypeError):
            self.service.login_user()

    # Hash täytyy testailla vielä
