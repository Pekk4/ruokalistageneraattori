from flask import redirect, render_template, Blueprint, request, session
from services.service import Service

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
