class User:
    def __init__(self, name: str, db_id: int = None):
        self.name = name
        self.db_id = db_id

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        return self.name == other.name and self.db_id == other.db_id
