import unittest
from unittest.mock import Mock
from repositories.base_repository import BaseRepository

class TestBaseRepository(unittest.TestCase):

    def setUp(self):
        self.database_mock = Mock()
        self.db_session_mock = Mock()
        self.return_on_select_mock = Mock()

        self.test_results = [Mock(name="Pizza"), Mock(name="Sillivoileipä")]
        self.credentials = {"username":"Paavo Pesusieni", "password":"Rapuleipä_666"}

        self._configure_mocks()

        self.repository = BaseRepository(self.database_mock)

        self.select_query = "SELECT name FROM meals"
        self.insert_query = "INSERT INTO users (username, password) VALUES (:username, :password)"
        self.param_select_query = "SELECT username, password FROM users WHERE username=:username"
        self.exception = Exception("Vituixmän")

    def _configure_mocks(self):
        self.db_session_mock.execute.return_value = self.return_on_select_mock
        self.return_on_select_mock.fetchall.return_value = self.test_results
        self.database_mock.attach_mock(self.db_session_mock, "session")

    def test_read_items_calls_database_methods_without_args(self):
        self.repository.read_items(self.select_query)

        self.db_session_mock.execute.assert_called_with(self.select_query, ())
        self.return_on_select_mock.fetchall.assert_called()

    def test_read_items_without_args_returns_correct_when_is_results(self):
        results = self.repository.read_items(self.select_query)

        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], Mock)
        self.assertEqual(results[0].name, self.test_results[0].name)

    def test_read_items_without_args_returns_correct_when_no_results(self):
        self.return_on_select_mock.fetchall.return_value = []
        result = self.repository.read_items(self.select_query)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_read_items_raises_exception_on_error(self):
        self.db_session_mock.execute.side_effect = self.exception

        with self.assertRaises(Exception) as error:
            self.repository.read_items(self.select_query)

        self.assertEqual(str(error.exception), "Vituixmän")

    def test_read_items_calls_database_methods_with_args(self):
        parameters = {"username":self.credentials["username"]}

        self.repository.read_items(self.param_select_query, parameters)

        self.db_session_mock.execute.assert_called_with(self.param_select_query, (parameters,))

    def test_read_items_with_args_returns_correct_when_is_results(self):
        result = self.repository.read_items(
            self.param_select_query,
            self.credentials["username"])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[1].name, self.test_results[1].name)

    def test_read_items_with_args_returns_correct_when_no_results(self):
        self.return_on_select_mock.fetchall.return_value = []
        result = self.repository.read_items(
            self.param_select_query,
            self.credentials["username"])

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_read_items_throws_exception_without_arguments(self):
        with self.assertRaises(TypeError):
            self.repository.read_items()

    def test_write_items_calls_database_methods_correct(self):
        self.repository.write_items(self.insert_query, self.credentials)

        self.db_session_mock.execute.assert_called_with(self.insert_query, self.credentials)
        self.db_session_mock.commit.assert_called()

    def test_write_items_on_exception(self):
        self.db_session_mock.execute.side_effect = self.exception

        with self.assertRaises(Exception) as error:
            self.repository.write_items(self.insert_query, self.credentials)

        self.assertEqual(str(error.exception), "Vituixmän")
