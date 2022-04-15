class Meal:
    def __init__(self, name, db_id=None):
        self.name = name
        self.id = db_id

    def __str__(self) -> str:
        return self.name
