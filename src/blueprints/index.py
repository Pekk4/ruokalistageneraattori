from datetime import datetime
from urllib.parse import urlparse

from flask import Blueprint, redirect, render_template, flash, request, session

from services.meal_service import MealService
from services.menu_service import MenuService
from utilities import DAYS, QTY_UNITS, check_session
from services.news_service import NewsService


index_blueprint = Blueprint("index_blueprint", __name__)
meal_service = MealService()
menu_service = MenuService()
news_service = NewsService()
day_indexes = list(range(7))

@index_blueprint.route("/")
def index():
    user_id = check_session(session, request)
    page = render_template("index.html")

    if user_id:
        menu = menu_service.fetch_menu(user_id)
        news = NewsService().get_news()

        if isinstance(news, str):
            news = []
        if isinstance(menu, str):
            return render_template("index.html", message=menu, news=news)
        if isinstance(menu, list):
            return render_template("index.html", menu=menu, news=news)

        page = render_template("index.html", menu=zip(menu.meals, day_indexes), news=news)

    return page

@index_blueprint.route("/generate")
def generate_menu():
    header_path = urlparse(request.referrer).path
    user_id = check_session(session, request)

    if user_id:
        message = menu_service.generate_menu(user_id)

        if message:
            flash(message)

    if header_path == "/manage":
        return redirect("/manage")

    return redirect("/")

@index_blueprint.route("/meals", methods=["GET"])
def view_meals():
    user_id = check_session(session, request)
    page = render_template("meal.html")

    if user_id:
        meals = meal_service.fetch_user_meals(user_id)
        ingredients = meal_service.fetch_user_ingredients(user_id)

        if isinstance(meals, str):
            return render_template("meal.html", message=meals)

        if "new" in request.args:
            return render_template(
                "meal.html",
                insert_mode=True,
                meals=meals,
                ingredients=ingredients
            )

        page = render_template("meal.html", meals=meals, ingredients=ingredients)

    return page

@index_blueprint.route("/meal/")
@index_blueprint.route("/meal/<int:meal_id>")
def view_meal(meal_id=None):
    page = render_template("meal.html")

    if meal_id:
        user_id = check_session(session, request)

        if user_id:
            meal = meal_service.fetch_single_meal(user_id, meal_id=meal_id)
            meals = meal_service.fetch_user_meals(user_id)
            ingredients = meal_service.fetch_user_ingredients(user_id)

            if isinstance(meal, str):
                return render_template("meal.html", message=meal)
            if isinstance(meals, str):
                return render_template("meal.html", message=meals)

            page = render_template("meal.html", meal=meal, meals=meals, ingredients=ingredients, update=True)

        return page

    return redirect("/")

@index_blueprint.route("/manage")
def manage_menus():
    user_id = check_session(session, request)
    page = render_template("manage.html")

    if user_id:
        menu = menu_service.fetch_menu(user_id)
        older_menus = menu_service.fetch_old_menus(user_id, 35)

        if isinstance(menu, str):
            return render_template("manage.html", message=menu)
        if isinstance(older_menus, str):
            return render_template("manage.html", message=older_menus)
        if isinstance(menu, list):
            return render_template("manage.html", older_menus=older_menus, menu=menu)

        page = (
            render_template(
                "manage.html",
                old_menus=older_menus,
                menu=zip(menu.meals, day_indexes)
            )
        )

    return page

@index_blueprint.route("/old_menus", methods=["GET"])
def view_old_menus():
    user_id = check_session(session, request)
    page = render_template("old_menus.html")

    if user_id:
        menus = menu_service.fetch_old_menus(user_id)

        if isinstance(menus, str):
            return render_template("old_menus.html", message=menus)

        if request.args:
            selected_menu = (
                menu_service.fetch_menu_by_timestamp(
                    user_id,
                    request.args.get("week"),
                    request.args.get("year")
                )
            )

            if isinstance(selected_menu, str):
                return render_template("old_menus.html", message=selected_menu, menus=menus)

            return render_template(
                "old_menus.html",
                menus=menus,
                timestamp=selected_menu.timestamp.isocalendar(),
                selected_menu=zip(selected_menu.meals, day_indexes)
            )

        page = render_template("old_menus.html", menus=menus)

    return page

@index_blueprint.route("/news/")
@index_blueprint.route("/news/<int:news_id>")
def news(news_id=None):
    if news_id:
        user_id = check_session(session, request)

        if user_id:
            news = news_service.get_single_news(news_id)

            return render_template("news.html", news=news)

    return redirect("/")

@index_blueprint.route("/shopping_list")
def shopping_list():
    user_id = check_session(session, request)

    if user_id:
        ingredients = menu_service.fetch_menus_ingredients(user_id)

        if not isinstance(ingredients, str):
            return render_template("shopping_list.html", ingredients=ingredients)

        return redirect("/manage")

    return redirect("/")

@index_blueprint.context_processor
def utilities():
    return dict(today=datetime.today(), days=DAYS, day_numbers=list(range(7)), qty_units=QTY_UNITS)
