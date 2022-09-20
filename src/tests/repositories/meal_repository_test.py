import unittest
from unittest.mock import patch

from entities.meal import Meal
from entities.errors import InsertingError
from repositories.meal_repository import MealRepository


class TestMealRepository(unittest.TestCase):
    def setUp(self):
        self.repository = MealRepository()
        self.meal_parameters = {"meal":"Surströmming och pepparkakor"}
        self.ingredients = ["Porkkana", "Päärynä"]
        self.ingredient_ids = [(666,), (777,), (888,)]

    @patch("repositories.io.InputOutput.read")
    def test_find_all_meals_calls_read_method_correct(self, read_mock):
        self.repository.find_all_meals()

        read_mock.assert_called_with("SELECT name, id FROM meals")

    @patch("repositories.io.InputOutput.read")
    def test_find_all_meals_does_not_call_read_method_incorrect(self, read_mock):
        self.repository.find_all_meals()

        self.assertFalse("SELECT * FROM meals" in read_mock.call_args.args)

    @patch("repositories.io.InputOutput.read")
    def test_find_all_meals_returns_correct_when_no_results(self, read_mock):
        read_mock.return_value = []

        result = self.repository.find_all_meals()

        self.assertEqual(len(result), 0)
        self.assertIsInstance(result, list)

    @patch("repositories.io.InputOutput.read")
    def test_find_all_meals_returns_correct_when_is_results(self, read_mock):
        read_mock.return_value = [Meal("Surströmming", 1), Meal("Pepparkakor", 2)]

        result = self.repository.find_all_meals()

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[1], Meal)
        self.assertEqual(result[0].name, "Surströmming")
        self.assertEqual(result[1].id, 2)

    @patch("repositories.io.InputOutput.write")
    def test_insert_meal_calls_write_method_correct(self, write_mock):
        query = "INSERT INTO meals (name) VALUES (:meal) RETURNING id"
        write_mock.return_value = (666,)

        self.repository.insert_meal(self.meal_parameters["meal"])

        write_mock.assert_called_with(query, self.meal_parameters)
        self.assertTrue(query in write_mock.call_args[0])

    @patch("repositories.io.InputOutput.write")
    def test_insert_meal_does_not_call_write_method_incorrect(self, write_mock):
        false_query = "INSERT INTO meal (name) VALUES (:meal) RETURNING id"
        write_mock.return_value = (666,)

        self.repository.insert_meal(self.meal_parameters["meal"])

        self.assertFalse(false_query in write_mock.call_args[0])

    @patch("repositories.io.InputOutput.write")
    def test_insert_meal_returns_correct_when_no_errors_occurred(self, write_mock):
        write_mock.return_value = (666,)

        self.assertEqual(self.repository.insert_meal("Kinuskikakku"), 666)

    @patch("repositories.io.InputOutput.write")
    def test_insert_meal_raises_exception_when_errors_occurred(self, write_mock):
        write_mock.return_value = False

        with self.assertRaises(InsertingError) as error:
            self.repository.insert_meal("Hapansilakkavoileivät")

        self.assertEqual(str(error.exception), "An error occurred during inserting meal, aborted.")

    @patch("repositories.io.InputOutput.write_many")
    def test_insert_ingredients_calls_write_many_method_correct(self, write_mock):
        query = "INSERT INTO ingredients (name) VALUES (:ingredient) RETURNING id"
        parameters = [{"ingredient":ingredient} for ingredient in self.ingredients]

        self.repository.insert_ingredients(self.ingredients)

        write_mock.assert_called_with(query, parameters)

    @patch("repositories.io.InputOutput.write_many")
    def test_insert_ingredients_does_not_call_write_many_method_incorrect(self, write_mock):
        false_query = "INSERT INTO meals (name) VALUES (:meal) RETURNING id"

        self.repository.insert_ingredients(self.ingredients)

        self.assertFalse(false_query in write_mock.call_args[0])

    @patch("repositories.io.InputOutput.write_many")
    def test_insert_ingredients_returns_correct_when_no_errors_occurred(self, write_mock):
        write_mock.return_value = self.ingredient_ids

        return_value = self.repository.insert_ingredients(self.ingredients)

        self.assertEqual(len(return_value), 3)
        self.assertIsInstance(return_value, list)

    @patch("repositories.io.InputOutput.write_many")
    def test_insert_ingredients_returns_correct_when_errors_occurred(self, write_mock):
        write_mock.return_value = False

        with self.assertRaises(InsertingError) as error:
            self.repository.insert_ingredients(self.ingredients)

        self.assertEqual(str(error.exception), "An error occurred during inserting ingredient, aborted.")

    @patch("repositories.io.InputOutput.write_many")
    def test_insert_meal_ingredients_calls_write_many_method_correct(self, write_mock):
        query = """
            INSERT INTO meal_ingredients (meal_id, ingredient_id)
            VALUES (:meal_id, :ingredient_id)"""
        parameters = [{"meal_id":666, "ingredient_id":db_id} for db_id, in self.ingredient_ids]

        self.repository.insert_meal_ingredients(666, self.ingredient_ids)

        write_mock.assert_called_with(query, parameters)

    @patch("repositories.io.InputOutput.write_many")
    def test_insert_meal_ingredients_does_not_call_write_many_method_incorrect(self, write_mock):
        false_query = "INSERT INTO meals (name) VALUES (:meal) RETURNING id"

        self.repository.insert_meal_ingredients(666, self.ingredient_ids)

        self.assertFalse(false_query in write_mock.call_args[0])

    @patch("repositories.io.InputOutput.write_many")
    def test_insert_meal_ingredients_returns_correct_when_no_errors_occurred(self, write_mock):
        write_mock.return_value = self.ingredient_ids

        self.assertTrue(self.repository.insert_meal_ingredients(666, self.ingredient_ids))

    @patch("repositories.io.InputOutput.write_many")
    def test_insert_meal_ingredients_returns_correct_when_errors_occurred(self, write_mock):
        write_mock.return_value = False

        with self.assertRaises(InsertingError) as error:
            self.repository.insert_meal_ingredients(666, self.ingredient_ids)

        self.assertEqual(str(error.exception), "An error occurred during inserting meal's ingredients, aborted.")
