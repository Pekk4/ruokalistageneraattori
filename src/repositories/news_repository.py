from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from repositories.io import InputOutput as default_io
from utils.errors import InsertingError, ReadDatabaseError
from entities.news import News


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

    #def find_single_news(self, news_id):
    #    query = "SELECT id, username, password FROM users WHERE username = :username"
    #    parameters = {"username":username}
    #
    #    try:
    #        return self.db_io.read(query, parameters)
    #    except SQLAlchemyError:
    #        raise ReadDatabaseError

    def find_all_news(self):
        query = "SELECT id, topic, news FROM news ORDER BY id DESC"

        try:
            return [News(news.topic, news.news, news.id) for news in self.db_io.read(query)]
        except SQLAlchemyError:
            raise ReadDatabaseError
