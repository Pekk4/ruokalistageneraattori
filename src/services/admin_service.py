from config import logfiles_path
from repositories.user_repository import UserRepository
from utils.errors import InsertingError, ReadDatabaseError
from utilities import MESSAGES

class AdminService:
    def __init__(self) -> None:
        self.repository = UserRepository()

    @staticmethod
    def get_logs():
        log_path = logfiles_path + "/db_errors.log"
        with open(log_path, "r") as file:
            logs = file.read().replace("\n", "<br />")

        return logs

    def get_users(self):
        try:
            return self.repository.find_all_users()
        except ReadDatabaseError:
            return MESSAGES["common_error"]

    def reset_password(self, user_id):
        try:
            self.repository.set_user_password(user_id)
        except InsertingError:
            return MESSAGES["common_error"]
