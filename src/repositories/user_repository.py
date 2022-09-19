from repositories.io import InputOutput as default_io
from entities.errors import InsertingError


class UserRepository():

    def __init__(self, database_io=default_io()):
        self.db_io = database_io

    def find_single_user(self, username):
        query = "SELECT username, password FROM users WHERE username=:username"
        parameters = {"username":username}

        return self.db_io.read(query, parameters)

    def add_user(self, username, password):
        query = "INSERT INTO users (username, password) VALUES (:username, :password)"
        parameters = {"username":username, "password":password}

        if not self.db_io.write(query, parameters):
            raise InsertingError("user")

        return True # Necessary?
