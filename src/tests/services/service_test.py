import unittest
from unittest.mock import Mock
from services.service import Service
from entities.meal import Meal

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
