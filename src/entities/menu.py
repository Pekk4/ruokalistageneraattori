class Menu:
    def __init__(self, meals: list, timestamp: str, db_id: int = False):
        if len(meals) < 7:
            raise ValueError("Seven meals required!")
        else:
            self.meals = meals
            self.timestamp = timestamp
            self.db_id = db_id or None

    def __repr__(self) -> str:
        return "Menu(" + str(self.meals) + ", " + str(self.timestamp) + ")"
