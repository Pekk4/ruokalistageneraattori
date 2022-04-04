import unittest
from unittest.mock import Mock
from entities.meal import Meal
from repositories.repository import Repository

class TestRepository(unittest.TestCase):

    def setUp(self):
        self.test_item_1 = Mock()
        self.test_item_2 = Mock()
        self.database_mock = Mock()
        self.db_session_mock = Mock()
        self.return_on_select_mock = Mock()

        self.test_results = [self.test_item_1, self.test_item_2]

        self._configure_mocks()

        self.repository = Repository(self.database_mock)

    def _configure_mocks(self):
        self.test_item_1.name = "Surströmming"
        self.test_item_2.name = "Pepparkakor"
        self.db_session_mock.execute.return_value = self.return_on_select_mock
        self.return_on_select_mock.fetchall.return_value = self.test_results
        self.database_mock.attach_mock(self.db_session_mock, "session")

    def test_find_all_meals_calls_database_methods(self):
        self.repository.find_all_meals()

        self.db_session_mock.execute.assert_called()
        self.return_on_select_mock.fetchall.assert_called()

    def test_find_all_meals_returns_correct_object_when_is_results(self):
        value = self.repository.find_all_meals()

        self.assertEqual(len(value), 2)
        self.assertIsInstance(value[0], Meal)
        self.assertEqual(value[0].name, self.test_item_1.name)

    def test_find_all_meals_returns_correct_object_when_no_results(self):
        self.return_on_select_mock.fetchall.return_value = []
        value = self.repository.find_all_meals()

        self.assertIsInstance(value, list)
        self.assertEqual(len(value), 0)

    def test_find_all_meals_on_exception(self):
        self.db_session_mock.execute.side_effect = Exception('Vituixmän')

        with self.assertRaises(Exception) as error:
            self.repository.find_all_meals()

        self.assertEqual(str(error.exception), "Vituixmän")
