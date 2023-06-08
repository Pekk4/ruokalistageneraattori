from config import logfiles_path
from repositories.user_repository import UserRepository


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
        return self.repository.find_all_users()
