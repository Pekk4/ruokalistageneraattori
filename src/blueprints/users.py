from flask import redirect, render_template, Blueprint, request, session
from secrets import token_hex

from services.service import Service


service = Service()
users_blueprint = Blueprint("login_blueprint", __name__)

@users_blueprint.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = service.login_user(username, password)

    if user:
        (uname, uid) = user

        session["username"] = uname
        session["uid"] = uid
        session["token"] = token_hex(32)

    return redirect("/")

@users_blueprint.route("/logout")
def logout():
    del session["username"]
    del session["uid"]
    del session["token"]

    return redirect("/")

@users_blueprint.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    service.insert_new_user(username, password)

    return redirect("/")

@users_blueprint.route("/login_page")
def login_page():
    return render_template("login.html")

@users_blueprint.route("/register_page")
def register_page():
    return render_template("register.html")
