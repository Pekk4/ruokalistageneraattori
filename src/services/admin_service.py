from config import logfiles_path
from repositories.user_repository import UserRepository
from utils.errors import InsertingError, ReadDatabaseError
from utilities import MESSAGES
from repositories.news_repository import NewsRepository


class AdminService:
    def __init__(self) -> None:
        self.user_repository = UserRepository()
        self.news_repository = NewsRepository()

    @staticmethod
    def get_logs():
        log_path = logfiles_path + "/db_errors.log"
        with open(log_path, "r") as file:
            logs = file.read().replace("\n", "<br />")

        return logs

    def get_users(self):
        try:
            return self.user_repository.find_all_users()
        except ReadDatabaseError:
            return MESSAGES["common_error"]

    def reset_password(self, user_id):
        try:
            self.user_repository.set_user_password(user_id)
        except InsertingError:
            return MESSAGES["common_error"]

    def insert_news(self, news_data):
        try:
            self.news_repository.add_news(news_data["topic"], news_data["news"])
        except InsertingError:
            return MESSAGES["common_error"]

    def get_news(self):
        try:
            return self.news_repository.find_all_news()
        except ReadDatabaseError:
            return MESSAGES["common_error"]
