from flask import redirect, render_template, Blueprint, request, session
from services.service import Service

index_blueprint = Blueprint("index_blueprint", __name__)

serv = Service()

@index_blueprint.route("/")
def index():
    meals = serv.fetch_menu()

    return render_template("index.html", meals=meals)

@index_blueprint.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@index_blueprint.route("/generate")
def generate():
    serv.generate_menu()

    return redirect("/")

@index_blueprint.route("/meals")
def meals():
    meals = serv.fetch_meals()

    return render_template("add_meal.html", meals=meals)

@index_blueprint.route("/add_meal", methods=["POST"])
def add_meal():
    serv.add_meal(request.form.to_dict())

    return redirect("/meals")
