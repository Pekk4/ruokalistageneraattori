from flask import Flask
from flask_wtf.csrf import CSRFProtect
from talisman import Talisman

from config import DATABASE_URL, SECRET_KEY, CSP
from database import database
from blueprints.admin import admin_blueprint
from blueprints.index import index_blueprint
from blueprints.users import users_blueprint
from blueprints.interfaces import interfaces_blueprint


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = SECRET_KEY

Talisman(
    app,
    content_security_policy=CSP
)

csrf = CSRFProtect()
csrf.init_app(app)
database.init_app(app)

app.register_blueprint(admin_blueprint)
app.register_blueprint(index_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(interfaces_blueprint)
