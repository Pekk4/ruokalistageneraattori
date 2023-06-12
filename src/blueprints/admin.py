from flask import Blueprint, render_template, request, session

from services.admin_service import AdminService
from utilities import check_session


admin_blueprint = Blueprint("admin_blueprint", __name__)
admin_service = AdminService()

@admin_blueprint.route("/admin")
def admin():
    user_id = check_session(session, request)

    if user_id and user_id == 1:
        logs = admin_service.get_logs()

        return render_template("logs.html", logs=logs, paska=True)
    
    return render_template("index.html")

@admin_blueprint.route("/users")
def users():
    user_id = check_session(session, request)

    if user_id and user_id == 1:
        users = admin_service.get_users()

        return render_template("users.html", users=users)

    return render_template("index.html")

@admin_blueprint.route("/reset_password", methods=["GET"])
def reset_password():
    user_id = check_session(session, request)

    if user_id and user_id == 1:
        status = admin_service.reset_password(request.args.get("id"))

        if isinstance(status, str):
            return status, 500
        
        return "OK", 200

    return "\N{angry face}", 403
