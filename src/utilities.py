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

MESSAGES = {
    "no_meals":
        "Sinulla ei ole vielä yhtään ruokalajia. \N{slightly frowning face}<br>" \
        "<br>Lisää ensin ruokalajeja kirjastoosi generoidaksesi niistä ruokalistan.",
    "common_error":
        "Jotain meni valitettavasti pieleen. \N{crying face}<br>" \
        "<br>Yritä hetken päästä uudestaan, tai ota yhteyttä ylläpitoon.",
    "input_error":
        "Tyhjät merkkijonot niminä eivät ole sallittuja. \N{angry face}",
    "meal_exists":
        "Samanniminen ruokalaji löytyy jo kirjastostasi, " \
        "haluatko päivittää sen antamillasi tiedoilla?",
    "not_enough":
        "Kirjastossasi ei ole tarpeeksi ruokalajeja ruokalistan luomiseksi." \
        "Lisää ensin ruokalajeja kirjastoosi.",
    "no_user":
        "Käyttäjätunnusta ei löydy, tarkista kirjoitusasu. \N{crying face}",
    "wrong_pass":
        "Väärä salasana, yritä uudestaan. \N{face with monocle}",
    "invalid_pass":
        "Salasana ei ole kelvollinen, noudata annettuja ohjeita! \N{angry face}",
    "invalid_uname":
        "Käyttäjänimi ei ole kelvollinen, noudata annettuja ohjeita! \N{angry face}",
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

def check_session(session, request):
    if "uid" in session:
        if (session["uagent"] == request.user_agent.string
                and session["remote_addr"] == request.remote_addr):

            return session["uid"]
        else:
            session.clear()

    return False
