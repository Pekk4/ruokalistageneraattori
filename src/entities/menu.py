class Menu:

    def __init__(self, meals: list, timestamp, db_id=False):
        if len(meals) < 7:
            raise ValueError("Seven meals required!")
        else:
            self.meals = meals
            self.timestamp = timestamp
            self.db_id = db_id or None

    def __repr__(self) -> str:
        return "Menu(" + str(self.meals) + ", " + str(self.timestamp) + ")"
