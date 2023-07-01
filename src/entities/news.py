class News:
    def __init__(self, topic: str, news: str, date: str, db_id: int = None):
        self.topic = topic
        self.news = news
        self.db_id = db_id
        self.date = date

    def __str__(self) -> str:
        return self.topic

    def __eq__(self, other: object) -> bool:
        return self.topic == other.topic and self.db_id == other.db_id
