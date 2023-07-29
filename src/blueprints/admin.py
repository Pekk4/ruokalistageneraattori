from flask import Blueprint, render_template, request, session, redirect, flash

from services.user_service import UserService
from services.news_service import NewsService
from utilities import check_session, read_logs


admin_blueprint = Blueprint("admin_blueprint", __name__)
user_service = UserService()
news_service = NewsService()

@admin_blueprint.route("/logs")
def get_logs():
    (user_id, is_admin) = check_session(session, request, True)

    if user_id and is_admin:
        logs = read_logs()

        return render_template("logs.html", logs=logs)

    return render_template("index.html")

@admin_blueprint.route("/users")
def get_users():
    (user_id, is_admin) = check_session(session, request, True)

    if user_id and is_admin:
        users = user_service.get_users()

        if isinstance(users, str):
            return render_template("users.html", message=users)

        return render_template("users.html", users=users)

    return render_template("index.html")

@admin_blueprint.route("/reset_password", methods=["GET"])
def reset_password():
    (user_id, is_admin) = check_session(session, request, True)

    if user_id and is_admin:
        status = user_service.reset_password(request.args.get("id"))

        if isinstance(status, str):
            return status, 500

        return "OK", 200

    return "\N{angry face}", 403

@admin_blueprint.route("/admin_news")
def admin_news():
    (user_id, is_admin) = check_session(session, request, True)

    if user_id and is_admin:
        news = news_service.get_news()

        if isinstance(news, str):
            flash(news)

            return redirect("/logs")

        return render_template("admin_news.html", news=news)

    return render_template("index.html")

@admin_blueprint.route("/submit_news", methods=["POST"])
def submit_news():
    (user_id, is_admin) = check_session(session, request, True)

    if user_id and is_admin:
        news_data = {
            "topic": request.form["topic"],
            "news": request.form["news"]
        }

        status = news_service.insert_news(news_data)

        if isinstance(status, str):
            flash(status)
        else:
            flash("Uutisen lisäys onnistui!")

        return redirect("/admin_news")

    return "\N{angry face}", 403
