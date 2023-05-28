from config import logfiles_path


class AdminService:
    def get_logs(self):
        log_path = logfiles_path + "/db_errors.log"
        with open(log_path, "r") as file:
            logs = file.read().replace("\n", "<br />")

        return logs
