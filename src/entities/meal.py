class Meal:
    def __init__(self, name: str, ingredients: list = None, db_id: int = None):
        self.name = name
        self.db_id = db_id
        self.ingredients = ingredients

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        return self.name == other.name# and self.ingredients == other.ingredients
