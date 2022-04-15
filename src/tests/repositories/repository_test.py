import unittest
from unittest.mock import patch
from entities.meal import Meal
from repositories.repository import Repository

class TestRepository(unittest.TestCase):

    def setUp(self):
        self.repository = Repository(None)

    @patch("repositories.base_repository.BaseRepository.read_items")
    def test_find_all_meals_calls_super_object_correctly(self, patched_mock):
        self.repository.find_all_meals()

        patched_mock.assert_called_with("SELECT name, id FROM meals")

    @patch("repositories.base_repository.BaseRepository.read_items")
    def test_find_all_meals_returns_correct_when_no_results(self, patched_mock):
        patched_mock.return_value = []

        result = self.repository.find_all_meals()

        self.assertEqual(len(result), 0)
        self.assertIsInstance(result, list)

    @patch("repositories.base_repository.BaseRepository.read_items")
    def test_find_all_meals_returns_correct_when_is_results(self, patched_mock):
        patched_mock.return_value = [Meal("Surströmming"), Meal("Pepparkakor")]

        result = self.repository.find_all_meals()

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[1], Meal)
        self.assertEqual(result[0].name, "Surströmming")

    @patch("repositories.base_repository.BaseRepository.write_items")
    def test_add_user_calls_super_object_correctly(self, patched_mock):
        query = "INSERT INTO users (username, password) VALUES (:username, :password)"
        parameters = {"username":"Aku Ankka", "password":"Pulivari313"}

        self.repository.add_user(parameters["username"], parameters["password"])

        patched_mock.assert_called_with(query, parameters)

    @patch("repositories.base_repository.BaseRepository.write_items")
    def test_add_user_super_method_with_incorrect_assertion(self, patched_mock):
        parameters = {"username":"Aku Ankka", "password":"Pulivari313"}

        self.repository.add_user(parameters["username"], parameters["password"])

        with self.assertRaises(AssertionError):
            
            patched_mock.assert_called_with("Any key...")

    @patch("repositories.base_repository.BaseRepository.read_items")
    def test_find_single_user_calls_super_object_correctly(self, patched_mock):
        query = "SELECT username, password FROM users WHERE username=:username"
        parameters = {"username":"Tohtori Sykerö"}

        self.repository.find_single_user(parameters["username"])

        patched_mock.assert_called_with(query, parameters)

    @patch("repositories.base_repository.BaseRepository.read_items")
    def test_find_single_user_returns_correct_object_when_no_results(self, patched_mock):
        patched_mock.return_value = []

        result = self.repository.find_single_user("Komisario Palmu")

        self.assertEqual(len(result), 0)
        self.assertIsInstance(result, list)

    @patch("repositories.base_repository.BaseRepository.read_items")
    def test_find_single_user_returns_correct_object_when_is_results(self, patched_mock):
        patched_mock.return_value = [666]

        result = self.repository.find_single_user("Mustakaapu")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 666)
