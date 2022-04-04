from repositories.repository import Repository as default_repository

class Service:
    def __init__(self, repository=default_repository()):
        self.repository = repository

    def provide_meals(self):
        meals = self.repository.find_all_meals()

        return meals
