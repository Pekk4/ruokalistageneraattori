from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from repositories.io import InputOutput as default_io
from utils.errors import InsertingError, ReadDatabaseError


class NewsRepository():
    def __init__(self, database_io=default_io()):
        self.db_io = database_io

    def add_news(self, topic, news):
        query = "INSERT INTO news (topic, news) VALUES (:topic, :news)"
        parameters = {"topic": topic, "news": news}

        try:
            return_value = self.db_io.write(query, parameters)
        except (IntegrityError, SQLAlchemyError):
            raise InsertingError("news")

        if not return_value:
            raise InsertingError("news")
