import logging
import logging.config
from sqlalchemy.exc import SQLAlchemyError

from database import database as default_db
from config import LOGGER_CONFIG_FILE as default_logger_path


class InputOutput:
    def __init__(self, database=default_db):
        logging.config.fileConfig(fname=default_logger_path)

        self.logger = logging.getLogger("dbLogger")
        self.session = database.session

    def read(self, query, *parameters):
        try:
            rows = self.session.execute(query, *parameters)
            results = rows.fetchall()

            return results

        except SQLAlchemyError as error: # katsotaan nyt, mitä tälle vielä sitten tehdään :|
            self.logger.error(error)
            return []

    def write(self, query, *parameters):
        try:
            return_value = self.session.execute(query, *parameters)
            self.session.commit()

            if "RETURNING" in query:
                return return_value.fetchone()

            return None

        except SQLAlchemyError as error: # sama juttu
            self.logger.error(error)
            return False

    def write_many(self, query, parameters: list):
        try:
            return_value = []

            if "RETURNING" in query:
                for parameter in parameters:
                    return_value.append(self.session.execute(query, parameter).fetchone())

            else:
                for parameter in parameters:
                    self.session.execute(query, parameter)

            self.session.commit()
            return return_value

        except SQLAlchemyError as error: # ja sama juttu
            self.logger.error(error)
            return False
