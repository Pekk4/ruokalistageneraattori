from flask import redirect, Blueprint, request, session, flash

from services.user_service import UserService
from utilities import check_session


service = UserService()
users_blueprint = Blueprint("users_blueprint", __name__)

@users_blueprint.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = service.login_user(username, password)

    if isinstance(user, int):
        session["reset"] = True
        session["uid"] = user
        session["uagent"] = request.user_agent.string
        session["remote_addr"] = request.remote_addr

        flash("Salasanasi on resetoitu, aseta uusi salasana.")

        return redirect("/")
    if isinstance(user, tuple):
        (uname, uid, is_admin) = user

        session["username"] = uname
        session["uid"] = uid
        session["uagent"] = request.user_agent.string
        session["remote_addr"] = request.remote_addr
        session["admin"] = is_admin
    else:
        flash(user)

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

    if message and not isinstance(message, bool):
        flash(message)

    return redirect("/")

@users_blueprint.route("/password", methods=["POST"])
def reset_password():
    user_id = check_session(session, request)

    if user_id:
        service.change_password(user_id, request.form["password"])

        session.clear()

    return redirect("/")
