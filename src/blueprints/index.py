from flask import redirect, render_template, Blueprint, session
from services.service import Service

index_blueprint = Blueprint("index_blueprint", __name__)

serv = Service()

@index_blueprint.route("/")
def index():
    meals = serv.provide_meals()

    return render_template("index.html", meals=meals)

@index_blueprint.route("/test")
def test():
    value = serv.insert_new_user()
    return str(value)

@index_blueprint.route("/logout")
def logout():
    del session["username"]
    return redirect("/")