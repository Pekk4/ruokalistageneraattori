#from flask import render_template, request, redirect
from flask import *
#from app import app
#from db import db
#from repositories.repository import Repository
from services.service import Service

example_blueprint = Blueprint("example_blueprint", __name__)

#repo = Repository()
serv = Service()

@example_blueprint.route("/")
def index():
    #meals = repo.find_all_meals()
    meals = serv.provide_meals()

    return render_template("index.html", meals=meals)
