from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from repositories.io import InputOutput as default_io
from utils.errors import InsertingError, ReadDatabaseError
from entities.news import News


class NewsRepository():
    def __init__(self, database_io=default_io()):
        self.db_io = database_io

    def add_news(self, topic, news):
        query = "INSERT INTO news (topic, news, date) VALUES (:topic, :news, NOW())"
        parameters = {"topic": topic, "news": news}

        try:
            return_value = self.db_io.write(query, parameters)
        except (IntegrityError, SQLAlchemyError) as original_error:
            raise InsertingError("news") from original_error

        if not return_value:
            raise InsertingError("news")

    def find_single_news(self, news_id):
        query = """
            SELECT id, topic, news, TO_CHAR(date, 'dd.mm.yyyy') as date
            FROM news WHERE id = :id"""
        parameters = {"id":news_id}

        try:
            result = self.db_io.read(query, parameters)

            if result:
                news = result[0]

                result = News(news.topic, news.news, news.date, news.id)

            return result

        except SQLAlchemyError as original_error:
            raise ReadDatabaseError from original_error

    def find_all_news(self):
        query = """
            SELECT id, topic, news, TO_CHAR(date, 'dd.mm.yyyy') as date
            FROM news ORDER BY date DESC, id DESC"""

        try:
            results = self.db_io.read(query)

            return [News(news.topic, news.news, news.date, news.id) for news in results]
        except SQLAlchemyError as original_error:
            raise ReadDatabaseError from original_error
