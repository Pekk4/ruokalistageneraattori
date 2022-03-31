import unittest
from unittest.mock import Mock
from repositories.repository import Repository
from services.service import Service

class TestService(unittest.TestCase):

    def setUp(self):
        self.database_mock = Mock()
        self.return_on_select_mock = Mock()

        self.repository_mock = Mock(wraps=Repository(self.database_mock))
        self.service = Service(self.repository_mock)

    def test_provide_meals_calls_repository_methods(self):
        self.service.provide_meals()

        self.repository_mock.find_all_meals.assert_called()

    def test_provide_meals_returns_correct_object(self):
        self.database_mock.session.execute.return_value = self.return_on_select_mock

        value = self.service.provide_meals()

        self.assertIsInstance(value, Mock)
        self.database_mock.session.execute.assert_called()
        self.return_on_select_mock.fetchall.assert_called()
