#from flask import render_template, request, redirect
from flask import *
from app import app
from repositories.repository import Repository


repo = Repository()

@app.route("/")
def index():
    meals = repo.find_all_meals()

    return render_template("index.html", meals=meals)
