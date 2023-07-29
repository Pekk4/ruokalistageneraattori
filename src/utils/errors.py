class InsertingError(Exception):
    def __init__(self, item: str):
        message = f"A technical error occurred during inserting {item}, please contact admin."

        super().__init__(message)

class ReadDatabaseError(Exception):
    def __init__(self):
        message = "Error occurred while reading items from database. Please see log file."

        super().__init__(message)

class NotEnoughMealsError(Exception):
    pass

class InvalidInputError(Exception):
    pass

class MealExistsWarning(Exception):
    pass

class NoResultsWarning(Exception):
    pass
