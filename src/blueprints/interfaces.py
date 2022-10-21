from datetime import datetime
import time
from urllib.parse import urlparse

from flask import redirect, render_template, Blueprint, request, session, abort, jsonify

from services.service import Service
from entities.errors import NotEnoughMealsError
from utilities import DAYS


interfaces_blueprint = Blueprint("interfaces_blueprint", __name__)
serv = Service()

@interfaces_blueprint.route("/get_meals")
def get_meals():
    if "uid" in session:
        meals = {meal.id:meal.name for meal in serv.fetch_users_meals(session["uid"])}

        try:
            mela = jsonify(meals)
            #time.sleep(3)
            return mela
        except NotEnoughMealsError:
            return ":("
    else:
        abort(403)

@interfaces_blueprint.route("/replace_meal", methods=["POST"])
def replace_meal():
    if "uid" in session:
        form_data = list(request.form.items())

        serv.replace_meal(session["uid"], form_data[0])

        print(list(request.form.items()))
        #time.sleep(3)
        return "OK"

@interfaces_blueprint.route("/generate_meal")
def generate_meal():
    if "uid" in session:
        meal = serv.generate_meal(session["uid"])

        return jsonify({"meal":meal.name, "id":meal.id})

@interfaces_blueprint.route("/old_menus", methods=["GET"])
def old_menus():
    if request.args:
        old_menus = serv.fetch_old_menus(session["uid"])
        selected_menu = serv.fetch_menu_by_timestamp(session["uid"], request.args.get("week"), request.args.get("year"))

        return render_template("old_menus.html", menus=old_menus, timestamp=selected_menu.timestamp.isocalendar(), sele_days=zip([i for i in range(7)], selected_menu.meals))
    else:
        old_menus = serv.fetch_old_menus(session["uid"])

        return render_template("old_menus.html", menus=old_menus)

@interfaces_blueprint.route("/replace_menu", methods=["GET"])
def replace_menu():
    if request.args:
        status = serv.replace_current_menu_with(session["uid"], request.args.get("week"), request.args.get("year"))

        if status is True:
            return "OK"

        return "NOK"


@interfaces_blueprint.route("/add_meal", methods=["POST", "GET"])
def add_meal():
    if "uid" in session:
        request_path = urlparse(request.referrer).path.split("/")
        meal_data = request.get_json()

        if request.args.get("update") == "true":
            meal_name = meal_data["meal_name"]
            status = serv.update_meal(session["uid"], meal_data, meal_name=meal_name)

            if isinstance(status, str):
                return status, 422
        else:
            if request_path[1] == "meal":
                meal_id = request_path[2]
                status = serv.update_meal(session["uid"], meal_data, meal_id=meal_id)
            if request_path[1] == "meals":
                status = serv.add_meal(session["uid"], meal_data)

            if isinstance(status, str):
                return status, 422

        return "OK"
    
    return "NOK"

@interfaces_blueprint.route("/delete_meal", methods=["POST"])
def delete_meal():
    if "uid" in session:
        meal = request.get_json()
        origin_path = urlparse(request.referrer).path.split("/")
        meal_id = origin_path[2]

        status = serv.delete_meal(session["uid"], meal_id, meal)

        if isinstance(status, str):
            return status, 422

    return "OK"

@interfaces_blueprint.context_processor
def testitee():
    return dict(today=datetime.today(), days=DAYS)


@interfaces_blueprint.route("/ammu")
def ammu():
    serv.ammu()

    return "OK"
