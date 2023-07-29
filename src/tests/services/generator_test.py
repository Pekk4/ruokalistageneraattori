import unittest
from unittest.mock import Mock
from datetime import datetime

from freezegun import freeze_time

from services.generator import GeneratorService, NotEnoughMealsError
from entities.menu import Menu
from entities.meal import Meal


class TestService(unittest.TestCase):
    def setUp(self):
        self.repository_mock = Mock()
        self.service = GeneratorService(self.repository_mock)

        self.meals = [Meal("Surströmming"+f"{i}") for i in range(7)]
        self.menu = Menu(self.meals, datetime.now())
        self.repository_mock.find_all_meals.return_value = self.meals

    def test_generate_menu_calls_repository_method(self):
        self.service.generate_menu(1)

        self.repository_mock.find_all_meals.assert_called_with(1)

    def test_generate_menu_raises_exception_when_too_few_meals_in_database(self):
        self.meals.pop()
        self.repository_mock.find_all_meals.return_value = self.meals

        with self.assertRaises(NotEnoughMealsError) as error:
            self.service.generate_menu(1)

        self.assertEqual(str(error.exception), "Not enough meals in the database")

    def test_generate_menu_returns_correct_object(self):
        menu = self.service.generate_menu(1)

        self.assertIsInstance(menu, Menu)

    @freeze_time("2012-01-14 12:00:01")
    def test_generate_menu_returned_menu_object_has_correct_details(self):
        menu = self.service.generate_menu(1)

        self.assertEqual(len(menu.meals), 7)
        self.assertIsInstance(menu.meals[0], Meal)
        self.assertEqual(menu.timestamp, datetime.now())

    def test_generate_menu_raffles_meals_to_menu(self):
        menu = self.service.generate_menu(1)

        with self.assertRaises(AssertionError):
            self.assertListEqual(self.meals, menu.meals)


    def prepare_meals(self):
        meals = self.meals.copy()

        meals.append(Meal("Sillisalaatti"))

        self.repository_mock.find_all_meals.return_value = meals

    def test_generate_meal_calls_repository_method(self):
        self.prepare_meals()
        self.service.generate_meal(1, self.menu)

        self.repository_mock.find_all_meals.assert_called_with(1)

    def test_generate_meal_raises_exception_when_too_few_meals_in_database(self):
        with self.assertRaises(NotEnoughMealsError) as error:
            self.service.generate_meal(1, self.menu)

        self.assertEqual(str(error.exception), "Not enough meals in the database")

    def test_generate_meal_returns_correct_object(self):
        self.prepare_meals()

        meal = self.service.generate_meal(1, self.menu)

        self.assertIsInstance(meal, Meal)

    def test_generate_meal_returns_meal_that_is_not_in_current_menu(self):
        self.prepare_meals()

        meal = self.service.generate_meal(1, self.menu)

        self.assertFalse(meal in self.menu.meals)
