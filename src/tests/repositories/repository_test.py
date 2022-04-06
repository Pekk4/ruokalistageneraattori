import unittest
from unittest.mock import Mock
from entities.meal import Meal
from repositories.repository import Repository

class TestRepository(unittest.TestCase):

    def setUp(self):
        self.io_mock = Mock()
        self.test_item_1 = Mock()
        self.test_item_2 = Mock()

        self.test_results = [self.test_item_1, self.test_item_2]
        self.credentials = {"username":"Paavo Pesusieni", "password":"Rapuleipä_666"}

        self.test_item_1.name = "Surströmming"
        self.test_item_2.name = "Pepparkakor"
        self.io_mock.read.return_value = self.test_results

        self.repository = Repository(self.io_mock)

    def test_find_all_meals_calls_read_correct(self):
        self.repository.find_all_meals()

        self.io_mock.read.assert_called_with("SELECT name FROM meals")

    def test_find_all_meals_returns_correct_when_is_results(self):
        results = self.repository.find_all_meals()

        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], Meal)
        self.assertEqual(results[0].name, self.test_item_1.name)

    def test_find_all_meals_returns_correct_when_no_results(self):
        self.io_mock.read.return_value = []
        result = self.repository.find_all_meals()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_find_all_meals_calls_does_not_call_read_incorrect(self):
        with self.assertRaises(AssertionError):
            self.io_mock.read.assert_called_with("Nönnönnöö")

    def test_find_all_meals_throws_exception_when_incorrect_result_type(self):
        self.io_mock.read.return_value = [None]

        with self.assertRaises(AttributeError):
            self.repository.find_all_meals()

    def test_add_user_calls_write_correct(self):
        query = "INSERT INTO users (username, password) VALUES (:username, :password)"

        self.repository.add_user(self.credentials["username"], self.credentials["password"])

        self.io_mock.write.assert_called_with(query, self.credentials)

    def test_add_user_throws_exception_without_arguments(self):
        with self.assertRaises(TypeError):
            self.repository.add_user()

    def test_find_single_user_calls_read_correct(self):
        query = "SELECT username, password FROM users WHERE username=:username"
        test_dict = {"username":self.credentials["username"]}

        self.repository.find_single_user(self.credentials["username"])

        self.io_mock.read.assert_called_with(query, test_dict)

    def test_find_single_user_returns_correct_when_is_results(self):
        result = self.repository.find_single_user(self.credentials["username"])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, self.test_item_1.name)
        self.assertNotIsInstance(result[0], Meal)

    def test_find_single_user_returns_correct_when_no_results(self):
        self.io_mock.read.return_value = []
        result = self.repository.find_all_meals()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_find_single_user_throws_exception_without_arguments(self):
        with self.assertRaises(TypeError):
            self.repository.find_single_user()
