import unittest
from unittest.mock import Mock
from repositories.io import InputOutput

class TestRepository(unittest.TestCase):

    def setUp(self):
        self.database_mock = Mock()
        self.db_session_mock = Mock()
        self.return_on_select_mock = Mock()

        self.test_results = [Mock(name="Pizza"), Mock(name="Tilliliha")]
        self.select_query = "SELECT name FROM meals"
        self.insert_query = "INSERT INTO users (username, password) VALUES (:username, :password)"
        self.variables = {"variable1":"Abrakadabra", "variable2":"Alohomora"}
        self.exception = Exception("Vituixmän")

        self._configure_mocks()

        self.input_output = InputOutput(self.database_mock)

    def _configure_mocks(self):
        self.db_session_mock.execute.return_value = self.return_on_select_mock
        self.return_on_select_mock.fetchall.return_value = self.test_results
        self.database_mock.attach_mock(self.db_session_mock, "session")

    def test_read_calls_database_methods_without_variables(self):
        self.input_output.read(self.select_query)

        self.db_session_mock.execute.assert_called_with(self.select_query, ())
        self.return_on_select_mock.fetchall.assert_called()

    def test_read_calls_database_methods_correctly_with_variables(self):
        self.input_output.read(self.select_query, self.variables)

        self.db_session_mock.execute.assert_called_with(self.select_query, (self.variables,))
        self.return_on_select_mock.fetchall.assert_called()

    def test_read_returns_correct_objects_without_variables(self):
        results = self.input_output.read(self.select_query)

        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], Mock)
        self.assertEqual(str(results[0]), str(self.test_results[0]))

    def test_read_returns_correct_objects_with_variables(self):
        results = self.input_output.read(self.select_query, self.variables)

        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], Mock)
        self.assertEqual(str(results[1]), str(self.test_results[1]))

    def test_read_on_exception(self):
        self.db_session_mock.execute.side_effect = self.exception

        with self.assertRaises(Exception) as error:
            self.input_output.read(self.select_query)

        self.assertEqual(str(error.exception), "Vituixmän")

    def test_write_calls_database_methods(self):
        self.input_output.write(self.insert_query, self.variables)

        self.db_session_mock.execute.assert_called_with(self.insert_query, self.variables)
        self.database_mock.commit.assert_called()

    def test_write_on_exception(self):
        self.db_session_mock.execute.side_effect = self.exception

        with self.assertRaises(Exception) as error:
            self.input_output.write(self.insert_query, self.variables)

        self.assertEqual(str(error.exception), "Vituixmän")

    def test_run_database_command_calls_database_methods(self):
        self.input_output.run_database_command(self.select_query)

        self.db_session_mock.execute.assert_called_with(self.select_query)
        self.database_mock.commit.assert_called()

    def test_run_database_command_on_exception(self):
        self.db_session_mock.execute.side_effect = self.exception

        with self.assertRaises(Exception) as error:
            self.input_output.run_database_command(self.select_query)

        self.assertEqual(str(error.exception), "Vituixmän")
