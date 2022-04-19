from argon2 import PasswordHasher
from services.generator import GeneratorService
from repositories.repository import Repository as default_repository
from repositories.menu_repository import MenuRepository as default_menu_repository


class Service:

    def __init__(
        self,
        repository=default_repository(),
        menu_repository=default_menu_repository(),
        generator=False
    ):
        self.repository = repository
        self.menu_repository = menu_repository
        self.password_hasher = PasswordHasher()
        self.generator = generator or GeneratorService(self.repository)

    def fetch_menu(self):
        meals = self.menu_repository.fetch_menu()

        return meals

    def generate_menu(self):
        menu = self.generator.generate()

        self.menu_repository.insert_menu(menu)

        return True

    def insert_new_user(self, username, password):
        hash_value = self.password_hasher.hash(password)

        self.repository.add_user(username, hash_value)

    def login_user(self, username, password):
        user = self.repository.find_single_user(username)

        try:
            return self.password_hasher.verify(user[0].password, password)
        except Exception:
            return False

    def add_meal(self, meal):
        self.repository.insert_meal(meal)
