from flask import redirect, render_template, Blueprint, request
from services.service import Service

service = Service()

register_blueprint = Blueprint("register_blueprint", __name__)

@register_blueprint.route("/register_page")
def register_page():
    return render_template("register.html")

@register_blueprint.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    service.insert_new_user(username, password)

    return redirect("/")
