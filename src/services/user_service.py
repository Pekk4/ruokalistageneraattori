import re

from argon2 import PasswordHasher
from argon2.exceptions import HashingError, VerifyMismatchError

from entities.errors import InsertingError, InvalidInputError, ReadDatabaseError
from repositories.user_repository import UserRepository as default_repository
from utilities import MESSAGES


class UserService:
    def __init__(self, user_repository=default_repository()):
        self.user_repository = user_repository
        self.password_hasher = PasswordHasher()

    def insert_new_user(self, username, password):
        try:
            self._validate_username(username)
            self._validate_password(password)

            hash_value = self.password_hasher.hash(password)

            self.user_repository.add_user(username, hash_value)
        except InvalidInputError as error:
            return str(error)
        except (InsertingError, HashingError):
            return MESSAGES["common_error"]

    def login_user(self, username, password):
        try:
            user = self.user_repository.find_single_user(username)

            if not user:
                return MESSAGES["no_user"]

            self.password_hasher.verify(user[0].password, password)

            return (user[0].username, user[0].id)

        except VerifyMismatchError:
            return MESSAGES["wrong_pass"]
        except ReadDatabaseError:
            return MESSAGES["common_error"]


    @staticmethod
    def _validate_username(username):
        if len(username.strip()) < 5 or len(username) > 16:
            raise InvalidInputError(MESSAGES["invalid_pass"])
    
    @staticmethod
    def _validate_password(password):
        if (len(password.strip()) < 8 or not re.match(".*[\d]+", password) or
            not re.match(".*[\W_]+", password)):

            raise InvalidInputError(MESSAGES["invalid_uname"])
