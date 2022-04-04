#from flask import render_template, request, redirect
from flask import *
from services.service import Service

example_blueprint = Blueprint("example_blueprint", __name__)

serv = Service()

@example_blueprint.route("/")
def index():
    meals = serv.provide_meals()

    return render_template("index.html", meals=meals)
