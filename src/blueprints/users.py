from flask import redirect, Blueprint, request, session, flash

from config import ADMIN_NAME
from services.user_service import UserService


service = UserService()
users_blueprint = Blueprint("login_blueprint", __name__)

@users_blueprint.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = service.login_user(username, password)

    if isinstance(user, tuple):
        (uname, uid) = user

        session["username"] = uname
        session["uid"] = uid
        session["uagent"] = request.user_agent.string
        session["remote_addr"] = request.remote_addr
    else:
        flash(user)

    return redirect("/admin") if user[0] == ADMIN_NAME else redirect("/")

    return redirect("/")

@users_blueprint.route("/logout")
def logout():
    session.clear()

    return redirect("/")

@users_blueprint.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    message = service.insert_new_user(username, password)

    if message:
        flash(message)

    return redirect("/")
