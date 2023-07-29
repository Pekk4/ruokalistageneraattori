from urllib.parse import urlparse

from flask import Blueprint, jsonify, request, session

from services.meal_service import MealService
from services.menu_service import MenuService
from services.user_service import UserService
from utilities import check_session


interfaces_blueprint = Blueprint("interfaces_blueprint", __name__)
meal_service = MealService()
menu_service = MenuService()
user_service = UserService()
message = "Please, log in first. \N{slightly smiling face}"

@interfaces_blueprint.route("/get_meals")
def get_meals():
    user_id = check_session(session, request)

    if user_id:
        meals = meal_service.fetch_user_meals(user_id)

        if isinstance(meals, list):
            return jsonify({meal.db_id:meal.name for meal in meals}), 200

        return meals, 500

    return message, 403

@interfaces_blueprint.route("/replace_meal", methods=["POST"])
def replace_meal():
    user_id = check_session(session, request)

    if user_id:
        form_data = list(request.form.items())
        status = menu_service.replace_meal(session["uid"], form_data[0])

        if isinstance(status, str):
            return status, 500

        return "OK", 201

    return message, 403

@interfaces_blueprint.route("/generate_meal")
def generate_meal():
    user_id = check_session(session, request)

    if user_id:
        meal = menu_service.generate_meal(user_id)

        if isinstance(meal, str):
            return meal, 500

        return jsonify({"meal":meal.name, "id":meal.db_id}), 200

    return message, 403

@interfaces_blueprint.route("/replace_menu", methods=["GET"])
def replace_menu():
    user_id = check_session(session, request)

    if user_id and request.args:
        args = request.args
        status = menu_service.replace_current_menu_with(user_id, args.get("week"), args.get("year"))

        if isinstance(status, str):
            return status, 500

        return "OK", 200

    return message, 403

@interfaces_blueprint.route("/add_meal", methods=["POST", "GET"])
def add_meal():
    user_id = check_session(session, request)

    if user_id:
        request_path = urlparse(request.referrer).path.split("/")
        meal_data = request.get_json()

        if request.args.get("update") == "true":
            meal_name = meal_data["meal_name"]
            status = meal_service.update_meal(user_id, meal_data, meal_name=meal_name)

            if isinstance(status, str):
                if "Samanniminen" in status:
                    return status, 422

                return status, 500
        else:
            if request_path[1] == "meal":
                meal_id = request_path[2]
                status = meal_service.update_meal(session["uid"], meal_data, meal_id=meal_id)
            if request_path[1] == "meals":
                status = meal_service.add_meal(session["uid"], meal_data)

            if isinstance(status, str):
                if "Samanniminen" in status:
                    return status, 422

                return status, 500

        return "OK", 201

    return message, 403

@interfaces_blueprint.route("/delete_meal", methods=["POST"])
def delete_meal():
    user_id = check_session(session, request)

    if user_id:
        meal = request.get_json()
        origin_path = urlparse(request.referrer).path.split("/")
        meal_id = origin_path[2]

        status = meal_service.delete_meal(user_id, meal_id, meal)

        if isinstance(status, str):
            return status, 500

        return "OK", 201

    return message, 403

@interfaces_blueprint.route("/check_username", methods=["GET"])
def check_username_availability():
    if request.args:
        status = user_service.check_username_availability(request.args.get("uname"))

        if isinstance(status, str):
            return status, 500

        return str(status), 200

    return ":)", 200
