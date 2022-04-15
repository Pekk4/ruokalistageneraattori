import unittest
from unittest.mock import Mock
from services.generator import GeneratorService, NotEnoughMealsError
from entities.menu import Menu


class TestService(unittest.TestCase):

    def setUp(self):
        self.repository_mock = Mock()
        self.service = GeneratorService(self.repository_mock)

        self.repository_mock.find_all_meals.return_value = list(range(0,7))

    def test_generate_calls_repository_methods(self):
        self.service.generate()

        self.repository_mock.find_all_meals.assert_called()

    def test_generate_raises_exception_when_too_least_meals_in_database(self):
        self.repository_mock.find_all_meals.return_value = list(range(0,6))

        with self.assertRaises(NotEnoughMealsError) as error:
            self.service.generate()

        self.assertEqual(str(error.exception), "Not enough meals in the database")

    def test_generate_returns_correct_object(self):
        menu = self.service.generate()

        self.assertIsInstance(menu, Menu)
        self.assertEqual(len(menu.meals), 7)
        self.assertIsInstance(menu.meals, list)
