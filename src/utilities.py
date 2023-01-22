from datetime import date


DAYS = {
    0: "Maanantai",
    1: "Tiistai",
    2: "Keskiviikko",
    3: "Torstai",
    4: "Perjantai",
    5: "Lauantai",
    6: "Sunnuntai",
}

QTY_UNITS = [
    "kpl",
    "mm",
    "tl",
    "rkl",
    "kkp",
    "ml",
    "dl",
    "l",
    "g",
    "kg",
    "pkt",
    "tlk",
    "rs",
    "pss"
]

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

def check_session(session, request):
    if "uid" in session:
        if (session["uagent"] == request.user_agent.string
                and session["remote_addr"] == request.remote_addr):

            return session["uid"]
        else:
            session.clear()

    return False
