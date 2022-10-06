from flask import redirect, render_template, Blueprint, request, session, abort, jsonify

from services.service import Service
from entities.errors import NotEnoughMealsError
from utilities import DAYS


index_blueprint = Blueprint("index_blueprint", __name__)
serv = Service()

@index_blueprint.route("/")
def index():
    if "uid" in session:
        meals = serv.fetch_menu(session["uid"])
    else:
        meals = []

    return render_template("index.html", meals=meals)

@index_blueprint.route("/generate")
def generate():
    if "uid" in session:
        serv.generate_menu(session["uid"])

    return redirect("/")

@index_blueprint.route("/meals")
def meals():
    if "uid" in session:
        meals = serv.fetch_users_meals(session["uid"])

    return render_template("add_meal.html", meals=meals)

@index_blueprint.route("/add_meal", methods=["POST"])
def add_meal():
    if "uid" in session:
        serv.add_meal(request.form.to_dict(), session["uid"])

    return redirect("/meals")

@index_blueprint.route("/manage")
def manage():
    if "uid" in session:
        menu = serv.fetch_menu(session["uid"])
        old_menus = serv.fetch_old_menus(session["uid"], 35)
    else:
        menu = []

    return render_template("manage.html", menus=old_menus, menumeals_days=zip(menu.meals,DAYS))

@index_blueprint.route("/get_meals")
def get_meals():
    if "uid" in session:
        meals = {meal.id:meal.name for meal in serv.fetch_users_meals(session["uid"])}

        try:
            mela = jsonify(meals)
            return mela
        except NotEnoughMealsError:
            return ":("
    else:
        abort(403)

@index_blueprint.route("/replace_meal", methods=["POST"])
def replace_meal():
    if "uid" in session:
        form_data = list(request.form.items())
        serv.replace_meal(session["uid"], form_data[0])

        return "OK"

@index_blueprint.route("/generate_meal")
def generate_meal():
    if "uid" in session:
        meal = serv.generate_meal(session["uid"])

        return jsonify({"meal":meal.name, "id":meal.id})

@index_blueprint.route("/old_menus", methods=["GET"])
def old_menus():
    if request.args:
        old_menus = serv.fetch_old_menus(session["uid"])
        selected_menu = serv.fetch_menu_by_timestamp(session["uid"], request.args.get("week"), request.args.get("year"))

        return render_template("old_menus.html", menus=old_menus, sele_days=zip(selected_menu.meals,DAYS))
    else:
        old_menus = serv.fetch_old_menus(session["uid"])

        return render_template("old_menus.html", menus=old_menus)

@index_blueprint.route("/replace_menu", methods=["GET"])
def replace_menu():
    if request.args:
        status = serv.replace_current_menu_with(session["uid"], request.args.get("week"), request.args.get("year"))

        if status is True:
            return "OK"

        return "NOK"
