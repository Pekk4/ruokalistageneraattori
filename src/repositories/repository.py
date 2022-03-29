class Repository:
    def __init__(self, db_obj):
        self.db = db_obj

    def find_all_meals(self):
        results = self.db.session.execute("SELECT name FROM meals")
        meals = results.fetchall()

        return meals
