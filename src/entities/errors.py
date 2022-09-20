class InsertingError(Exception):
    def __init__(self, item: str):
        message = f"An error occurred during inserting {item}, aborted."

        super().__init__(message)

class NotEnoughMealsError(Exception):
    pass
