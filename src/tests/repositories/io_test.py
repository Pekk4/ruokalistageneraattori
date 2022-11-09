import unittest
from unittest.mock import MagicMock, Mock
from sqlalchemy.exc import SQLAlchemyError

from repositories.io import InputOutput


class TestRepository(unittest.TestCase):
    def setUp(self):
        self.database_mock = Mock()
        self.db_session_mock = MagicMock()
        self.return_value_mock = Mock()

        self.test_results = [Mock(name="Pizza"), Mock(name="Tilliliha")]
        self.select_query = "SELECT name FROM meals"
        self.insert_query_1 = "INSERT INTO users (username, password) VALUES (:username, :password)"
        self.insert_query_2 = "INSERT INTO logins (time, user) VALUES (:time, :user) RETURNING id"
        self.query_variables = {"variable1":"Abrakadabra", "variable2":"Alohomora"}
        self.dict_list = [{"variable1":"Variaattori"}, {"variable2":"Separaattori"}]

        self._configure_mocks()

        self.input_output = InputOutput(self.database_mock)

    def _configure_mocks(self):
        self.db_session_mock.execute.return_value = self.return_value_mock
        self.return_value_mock.fetchall.return_value = self.test_results
        self.return_value_mock.fetchone.return_value = self.test_results

        self.database_mock.attach_mock(self.db_session_mock, "session")

    def test_read_calls_database_methods_correctly_without_variables(self):
        self.input_output.read(self.select_query)

        self.db_session_mock.execute.assert_called_with(self.select_query)
        self.return_value_mock.fetchall.assert_called()

    def test_read_calls_database_methods_correctly_with_variables(self):
        self.input_output.read(self.select_query, self.query_variables)

        self.db_session_mock.execute.assert_called_with(self.select_query, self.query_variables)
        self.return_value_mock.fetchall.assert_called()

    def test_read_returns_correct_objects_without_variables(self):
        results = self.input_output.read(self.select_query)

        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], Mock)
        self.assertEqual(str(results[0]), str(self.test_results[0]))

    def test_read_returns_correct_objects_with_variables(self):
        results = self.input_output.read(self.select_query, self.query_variables)

        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], Mock)
        self.assertEqual(str(results[1]), str(self.test_results[1]))

    def test_read_raises_exception_on_exception(self):
        self.return_value_mock.fetchall.side_effect = SQLAlchemyError

        with self.assertRaises(SQLAlchemyError):
            self.input_output.read(self.select_query)        

    def test_read_logging_on_exception(self):
        self.return_value_mock.fetchall.side_effect = SQLAlchemyError("Perskeles!")

        with self.assertRaises(SQLAlchemyError):
            with self.assertLogs() as logs:
                self.input_output.read(self.select_query)

        self.assertEqual(len(logs.records), 1)
        self.assertEqual(logs.records[0].getMessage(), "Perskeles!")

    def test_write_calls_database_methods(self):
        self.input_output.write(self.insert_query_1, self.query_variables)

        self.db_session_mock.execute.assert_called_with(self.insert_query_1, self.query_variables)
        self.db_session_mock.commit.assert_called()

    def test_write_calls_fetchone_with_returning_in_query(self):
        self.input_output.write(self.insert_query_2)

        self.return_value_mock.fetchone.assert_called()

    def test_write_returns_correct_with_returning_command_in_query(self):
        results = self.input_output.write(self.insert_query_2)

        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], Mock)
        self.assertEqual(str(results[0]), str(self.test_results[0]))

    def test_write_returns_correct_without_returning_command_in_query(self):
        self.assertTrue(self.input_output.write(self.insert_query_1))

    def test_write_raises_exception_on_exception(self):
        self.db_session_mock.commit.side_effect = SQLAlchemyError

        with self.assertRaises(SQLAlchemyError):
            self.input_output.write(self.insert_query_1)

    def test_write_logging_on_exception(self):
        self.db_session_mock.commit.side_effect = SQLAlchemyError("Tietokanta päreinä!")

        with self.assertRaises(SQLAlchemyError):
            with self.assertLogs() as logs:
                self.input_output.write(self.insert_query_1)

        self.assertEqual(len(logs.records), 1)
        self.assertEqual(logs.records[0].getMessage(), "Tietokanta päreinä!")

    def test_write_many_calls_database_methods_without_returning_command_in_query(self):
        self.input_output.write_many(self.insert_query_1, self.dict_list)

        self.db_session_mock.commit.assert_called()
        self.db_session_mock.execute.assert_called()

    def test_write_many_calls_database_commands_with_returning_command_in_query(self):
        self.input_output.write_many(self.insert_query_2, self.dict_list)

        returning_id = Mock()
        self.return_value_mock.execute.return_value = returning_id

        returning_id.fetchone_assert_called()
        self.db_session_mock.commit.assert_called()
        self.db_session_mock.execute.assert_called()

    def test_write_many_returns_correct_without_returning_command_in_query(self):
        return_value = self.input_output.write_many(self.insert_query_1, self.dict_list)

        self.assertEqual(len(return_value), 0)
        self.assertIsInstance(return_value, list)

    def test_write_many_returns_correct_with_returning_command_in_query(self):
        return_value = self.input_output.write_many(self.insert_query_2, self.dict_list)[0]

        self.assertIsInstance(return_value, list)
        self.assertEqual(len(return_value), len(self.test_results))
        self.assertEqual(str(self.test_results[0]), str(return_value[0]))

    def test_write_many_for_loops_without_returning_command_in_query(self):
        assumed_calls = [(self.insert_query_1, dict) for dict in self.dict_list]
        calls = self.db_session_mock.execute.call_args_list

        self.input_output.write_many(self.insert_query_1, self.dict_list)

        for i, call in enumerate(calls):
            args, *_ = call

            self.assertEqual(args, assumed_calls[i])

    def test_write_many_for_loops_with_returning_command_in_query(self):
        assumed_calls = [(self.insert_query_2, dict) for dict in self.dict_list]
        calls = self.db_session_mock.execute.call_args_list

        return_value = self.input_output.write_many(self.insert_query_2, self.dict_list)[0]

        for i, call in enumerate(calls):
            args, *_ = call

            self.assertEqual(args, assumed_calls[i])

        self.assertIsInstance(return_value, list)
        self.assertEqual(len(return_value), 2)
        self.assertEqual(str(return_value[0]), str(self.test_results[0]))

    def test_write_many_raises_exception_on_exception(self):
        self.db_session_mock.commit.side_effect = SQLAlchemyError

        with self.assertRaises(SQLAlchemyError):
            self.input_output.write_many(self.insert_query_1, self.dict_list)

    def test_write_many_logging_on_exception(self):
        self.db_session_mock.commit.side_effect = SQLAlchemyError("Tietokanta päreinä!")

        with self.assertRaises(SQLAlchemyError):
            with self.assertLogs() as logs:
                self.input_output.write_many(self.insert_query_1, self.dict_list)

        self.assertEqual(len(logs.records), 1)
        self.assertEqual(logs.records[0].getMessage(), "Tietokanta päreinä!")
