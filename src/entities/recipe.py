class Recipe:
    def __init__(self, name: str, meal: 'Meal', ingredients: list, recipe: str, db_id: int = None):
        self.name = name
        self.meal = meal
        self.ingredients = ingredients
        self.recipe = recipe
        self.db_id = db_id

    def __str__(self) -> str:
        return self.name

    def __eq__(self, __o: object) -> bool:
        return self.name == __o.name
