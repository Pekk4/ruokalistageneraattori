import unittest
from unittest.mock import Mock
from repositories.repository import Repository

class TestRepository(unittest.TestCase):

    def setUp(self):
        self.database_mock = Mock()
        self.return_on_select_mock = Mock()

        self.repository = Repository(self.database_mock)

    def test_find_all_meals_calls_database_methods(self):
        self.database_mock.session.execute.return_value = self.return_on_select_mock

        self.repository.find_all_meals()

        self.database_mock.session.execute.assert_called()
        self.return_on_select_mock.fetchall.assert_called()

    def test_find_all_meals_returns_correct_object(self):
        self.database_mock.session.execute.return_value = self.return_on_select_mock
        value = self.repository.find_all_meals()

        self.assertIsInstance(value, Mock)
        self.assertIs(value, self.return_on_select_mock.fetchall())
