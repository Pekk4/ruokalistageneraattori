from utils.errors import InsertingError, ReadDatabaseError
from utils.utilities import MESSAGES
from repositories.news_repository import NewsRepository


class NewsService:
    def __init__(self) -> None:
        self.repository = NewsRepository()

    def insert_news(self, news_data):
        try:
            self.repository.add_news(news_data["topic"], news_data["news"])
        except InsertingError:
            return MESSAGES["common_error"]

        return True

    def get_news(self):
        try:
            return self.repository.find_all_news()
        except ReadDatabaseError:
            return MESSAGES["common_error"]

    def get_single_news(self, news_id):
        try:
            return self.repository.find_single_news(news_id)
        except ReadDatabaseError:
            return MESSAGES["common_error"]
