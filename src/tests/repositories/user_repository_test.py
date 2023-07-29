import unittest
from unittest.mock import patch

from sqlalchemy.exc import SQLAlchemyError

from repositories.user_repository import UserRepository
from utils.errors import InsertingError, ReadDatabaseError
from entities.user import User


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.repository = UserRepository()
        self.select_query = "SELECT id, username, password FROM users WHERE username = :username"
        self.insert_query = "INSERT INTO users (username, password) VALUES (:username, :password)"
        self.parameters = {"username":"Matti", "password":"Meikäläinen_666"}

    @patch("repositories.io.InputOutput.read")
    def test_find_single_user_calls_read_method(self, read_mock):
        self.repository.find_single_user("Matti")

        read_mock.assert_called_with(self.select_query, {"username":"Matti"})

    @patch("repositories.io.InputOutput.read")
    def test_find_single_user_returns_correct_when_results(self, read_mock):
        read_mock.return_value = [("Matti", "Meikäläinen_666")]

        return_value = self.repository.find_single_user(self.parameters["username"])

        self.assertEqual(len(return_value), 1)
        self.assertIsInstance(return_value[0], tuple)

    @patch("repositories.io.InputOutput.read")
    def test_find_single_user_returns_correct_when_no_results(self, read_mock):
        read_mock.return_value = []

        return_value = self.repository.find_single_user(self.parameters["username"])

        self.assertEqual(len(return_value), 0)
        self.assertIsInstance(return_value, list)

    @patch("repositories.io.InputOutput.read")
    def test_find_single_user_raises_exception(self, read_mock):
        read_mock.side_effect = SQLAlchemyError("No db connection")

        with self.assertRaises(ReadDatabaseError):
            self.repository.find_single_user("Teppo")

    @patch("repositories.io.InputOutput.write")
    def test_add_user_calls_write_method(self, write_mock):
        self.repository.add_user(self.parameters["username"], self.parameters["password"])

        write_mock.assert_called_with(self.insert_query, self.parameters)

    @patch("repositories.io.InputOutput.write")
    def test_add_user_raises_exception_when_db_exception(self, write_mock):
        write_mock.side_effect = SQLAlchemyError
        error_text = "A technical error occurred during inserting user, please contact admin."

        with self.assertRaises(InsertingError) as error:
            self.repository.add_user(self.parameters["username"], self.parameters["password"])

        self.assertEqual(str(error.exception), error_text)

    @patch("repositories.io.InputOutput.write")
    def test_add_user_raises_exception_when_no_results(self, write_mock):
        write_mock.return_value = False

        with self.assertRaises(InsertingError) as error:
            self.repository.add_user(self.parameters["username"], self.parameters["password"])

        error_text = "A technical error occurred during inserting user, please contact admin."
        self.assertEqual(str(error.exception), error_text)

    @patch("repositories.io.InputOutput.read")
    def test_find_all_users_calls_read_method(self, read_mock):
        self.repository.find_all_users()

        read_mock.assert_called_with("SELECT id, username FROM users WHERE id NOT IN (1)")

    @patch("repositories.io.InputOutput.read")
    def test_find_all_users_returns_correct_when_results(self, read_mock):
        read_mock.return_value = [RowMock(1, "Groku")]

        return_value = self.repository.find_all_users()

        self.assertEqual(len(return_value), 1)
        self.assertEqual(return_value[0].name, "Groku")
        self.assertIsInstance(return_value[0], User)

    @patch("repositories.io.InputOutput.read")
    def test_find_all_users_raises_exception(self, read_mock):
        read_mock.side_effect = SQLAlchemyError("No db connection")

        with self.assertRaises(ReadDatabaseError):
            self.repository.find_all_users()

    @patch("repositories.io.InputOutput.write")
    def test_reset_password_calls_write_method(self, write_mock):
        query = "UPDATE users SET password = '' WHERE id = (:user_id)"

        self.repository.set_user_password(1)

        write_mock.assert_called_with(query, {"user_id":1})

    @patch("repositories.io.InputOutput.write")
    def test_reset_password_raises_exception_when_db_exception(self, write_mock):
        write_mock.side_effect = SQLAlchemyError
        error_text = "A technical error occurred during inserting reset, please contact admin."

        with self.assertRaises(InsertingError) as error:
            self.repository.set_user_password(1)

        self.assertEqual(str(error.exception), error_text)

    @patch("repositories.io.InputOutput.write")
    def test_reset_password_raises_exception_when_no_results(self, write_mock):
        write_mock.return_value = False

        with self.assertRaises(InsertingError) as error:
            self.repository.set_user_password(1)

        error_text = "A technical error occurred during inserting reset, please contact admin."
        self.assertEqual(str(error.exception), error_text)

    @patch("repositories.io.InputOutput.write")
    def test_set_password_calls_write_method_when_changing_password(self, write_mock):
        password = "lohileipälautanen666!"
        query = "UPDATE users SET password = (:password) WHERE id = (:user_id)"

        self.repository.set_user_password(1, password, False)

        write_mock.assert_called_with(query, {"user_id":1, "password":password})


class RowMock():
    def __init__(self, id, username,):
        self.id = id
        self.username = username