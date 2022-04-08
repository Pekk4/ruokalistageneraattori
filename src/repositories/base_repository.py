class BaseRepository:
    def __init__(self, database):
        self.connection = database

    def read_items(self, query, *params):
        results = self._read(query, *params)

        return results

    def write_items(self, query, parameters):
        self._write(query, parameters)

    def _read(self, query, *parameters):
        try:
            rows = self.connection.session.execute(query, parameters)
            results = rows.fetchall()

            return results

        except Exception: # pylint: disable=W0706
            raise

    def _write(self, query, *items):
        try:
            self.connection.session.execute(query, *items)
            self.connection.session.commit() # Piti olla session edessä

        except Exception: # pylint: disable=W0706
            raise

    def _run_database_command(self, query):
        try:
            self.connection.session.execute(query)
            self.connection.session.commit() # Piti olla session edessä

        except Exception: # pylint: disable=W0706
            raise
