from datetime import date


DAYS = {
    "Maanantai": 0,
    "Tiistai": 1,
    "Keskiviikko": 2,
    "Torstai": 3,
    "Perjantai": 4,
    "Lauantai": 5,
    "Sunnuntai": 6
}


def validate_week_number(week_number: int):
    weeks_this_year = date(date.today().year, 12, 28).isocalendar()[1]

    if 1 <= week_number <= weeks_this_year:
        return True

    raise ValueError("invalid week number")

def validate_year(year: int):
    current_year = date.today().year

    if 1970 <= year <= current_year:
        return True

    raise ValueError("invalid year")
