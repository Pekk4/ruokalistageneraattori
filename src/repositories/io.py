import logging
import logging.config

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

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

        except SQLAlchemyError as error:
            self.logger.error(error)
            raise

    def write(self, query, *parameters):
        try:
            return_value = self.session.execute(query, *parameters)
            self.session.commit()

            if "RETURNING" in query:
                return return_value.fetchone()

            return True

        except IntegrityError:
            raise
        except SQLAlchemyError as error:
            self.logger.error(error)
            raise

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

        except IntegrityError:
            raise
        except SQLAlchemyError as error:
            self.logger.error(error)
            raise
