from flask import Flask
from config import DATABASE_URL, SECRET_KEY
from database import database
from blueprints.index import index_blueprint
from blueprints.users import users_blueprint


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # tutki mihin nämä siivotaan tästä
    app.secret_key = SECRET_KEY


    database.init_app(app)

    app.register_blueprint(index_blueprint)
    app.register_blueprint(users_blueprint)

    return app

if __name__ == "__main__":
    app = create_app()
    #app.run(host="0.0.0.0", port="5000") #original, below is for testing loggers started with 'python3 app.py'
    app.run(host="0.0.0.0", port="5000", debug=False, use_debugger=False, use_reloader=False)
