from datetime import datetime
import time
from urllib.parse import urlparse

from flask import redirect, render_template, Blueprint, request, session, abort, jsonify, flash

from services.service import Service
from entities.errors import NotEnoughMealsError
from utilities import DAYS, QTY_UNITS


index_blueprint = Blueprint("index_blueprint", __name__)
serv = Service()

@index_blueprint.route("/")
def index():
    if "uid" in session:
        meals = serv.fetch_menu(session["uid"])

        if meals:
            return render_template("index.html", meals=zip(meals.meals, [i for i in range(7)]))
        else:
            return render_template("index.html", meals=[])

@index_blueprint.route("/generate")
def generate():
    header_path = urlparse(request.referrer).path

    if "uid" in session:
        serv.generate_menu(session["uid"])

        if header_path == "/manage":
            return redirect("/manage")

        return redirect("/")

@index_blueprint.route("/meals", methods=["GET"])
@index_blueprint.route("/meal/<int:meal_id>")
def meals(meal_id=None):
    if "uid" in session:
        insert_mode = request.args.get("new") or False
        meals = serv.fetch_user_meals(session["uid"])
        ingredients = serv.fetch_user_ingredients(session["uid"])

        if not meal_id and not insert_mode:
            return render_template("meal.html", meals=meals, ingredients=ingredients)
        elif insert_mode:
            return render_template("meal.html", insert_mode=True, meals=meals, ingredients=ingredients)
        else:
            meal = serv.fetch_single_meal(session["uid"], meal_id=meal_id)

            return render_template("meal.html", meal=meal, meals=meals, ingredients=ingredients)

@index_blueprint.route("/manage")
def manage():
    if "uid" in session:
        menu = serv.fetch_menu(session["uid"])
        old_menus = serv.fetch_old_menus(session["uid"], 35)
    else:
        menu = []

    return render_template("manage.html", menus=old_menus, menumeals=zip([i for i in range(7)], menu.meals))

@index_blueprint.route("/check_username", methods=["GET"])
def testitee():

    if request.args.get("uname") == "vittuu" or request.args.get("uname") == "vittu2":
        return "NOK"
    else:
        return "OK"

@index_blueprint.context_processor
def utilities():
    return dict(today=datetime.today(), days=DAYS, day_numbers=[i for i in range(7)], qty_units=QTY_UNITS)
