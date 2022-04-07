from argon2 import PasswordHasher
from repositories.repository import Repository as default_repository
from services.generator import GeneratorService

class Service:
    def __init__(self, repository=default_repository()):
        self.repository = repository
        self.generator = GeneratorService(self.repository)
        self.password_hasher = PasswordHasher()
    
    def fetch_meals(self):
        meals = self.repository.find_all_meals()

        return meals
    
    """def provide_meals(self):
        meals = self.generator.generate()

        return meals"""

    def insert_new_user(self, username, password):
        hash_value = self.password_hasher.hash(password)

        self.repository.add_user(username, hash_value)

    def login_user(self, username, password):
        user = self.repository.find_single_user(username)

        try:
            return self.password_hasher.verify(user[0].password, password)
        except Exception:
            return False
