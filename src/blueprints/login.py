from flask import redirect, render_template, Blueprint, request, session
from services.service import Service

service = Service()

login_blueprint = Blueprint("login_blueprint", __name__)

@login_blueprint.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if service.login_user(username, password):
        session["username"] = username

    return redirect("/")

@login_blueprint.route("/login_page")
def login_page():
    return render_template("login.html")
