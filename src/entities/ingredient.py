class Ingredient:
    def __init__(self, name: str, qty: int = None, qty_unit: str = None, db_id: int = None):
        self.name = name
        self.db_id = db_id
        self.qty = qty
        self.qty_unit = qty_unit

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        return self.name == other.name and self.qty == other.qty and self.qty_unit == other.qty_unit

    def __lt__(self, other: object):
        return self.name < other.name
