import unittest
from unittest.mock import Mock
from entities.meal import Meal
from repositories.repository import Repository

class TestRepository(unittest.TestCase):

    def setUp(self):
        self.database_mock = Mock()
        self.return_on_select_mock = Mock()

        self.meals = [Meal("Surströmming"), Meal("Pepparkakor")]

        self.database_mock.session.execute.return_value = self.return_on_select_mock
        self.return_on_select_mock.fetchall.return_value = self.meals

        self.repository = Repository(self.database_mock)

    def test_find_all_meals_calls_database_methods(self):
        self.repository.find_all_meals()

        self.database_mock.session.execute.assert_called()
        self.return_on_select_mock.fetchall.assert_called()

    def test_find_all_meals_returns_correct_object_when_is_results(self):
        
        value = self.repository.find_all_meals()

        self.assertEqual(len(value), 2)
        self.assertIsInstance(value[0], Meal)
        self.assertEqual(value[0].name, self.meals[0].name)

    def test_find_all_meals_returns_correct_object_when_no_results(self):
        self.return_on_select_mock.fetchall.return_value = []
        value = self.repository.find_all_meals()

        #self.assertIsNot(value, self.return_on_select_mock.fetchall())
        self.assertEqual(type(value), type([]))
        
