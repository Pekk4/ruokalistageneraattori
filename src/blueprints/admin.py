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
