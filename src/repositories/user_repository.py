from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from repositories.io import InputOutput as default_io
from utils.errors import InsertingError, ReadDatabaseError
from entities.user import User


class UserRepository():
    def __init__(self, database_io=default_io()):
        self.db_io = database_io

    def find_single_user(self, username):
        query = "SELECT id, username, password FROM users WHERE username = :username"
        parameters = {"username":username}

        try:
            return self.db_io.read(query, parameters)
        except SQLAlchemyError:
            raise ReadDatabaseError

    def add_user(self, username, password):
        query = "INSERT INTO users (username, password) VALUES (:username, :password)"
        parameters = {"username":username, "password":password}

        try:
            return_value = self.db_io.write(query, parameters)
        except (IntegrityError, SQLAlchemyError):
            raise InsertingError("user")

        if not return_value:
            raise InsertingError("user")

    def find_all_users(self):
        query = "SELECT id, username FROM users"

        try:
            return [User(user.username, user.id) for user in self.db_io.read(query)]
        except SQLAlchemyError:
            raise ReadDatabaseError
