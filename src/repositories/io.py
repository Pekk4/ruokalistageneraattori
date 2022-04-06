from database import database as default_db

class InputOutput:
    def __init__(self, database=default_db):
        self.connection = database

    def read(self, query, *variables):
        try:
            rows = self.connection.session.execute(query, variables)
            results = rows.fetchall()

            return results

        except Exception: # pylint: disable=W0706
            raise

    def write(self, query, items):
        try:
            self.connection.session.execute(query, items)
            self.connection.commit()

        except Exception: # pylint: disable=W0706
            raise

    def run_database_command(self, query):
        try:
            self.connection.session.execute(query)
            self.connection.commit()

        except Exception: # pylint: disable=W0706
            raise
