from database import database as default_db

class InputOutput:
    def __init__(self, database=default_db):
        self.session = database.session

    def read(self, query, *parameters):
        try:
            rows = self.session.execute(query, *parameters)
            results = rows.fetchall()

            return results

        except Exception: # pylint: disable=W0703
            return []

    def write(self, query, *parameters):
        try:
            return_value = self.session.execute(query, *parameters)
            self.session.commit()

            if "RETURNING" in query:
                return return_value.fetchone()

            return None

        except Exception: # pylint: disable=W0703
            return False
