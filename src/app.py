from flask import Flask
from config import DATABASE_URL
from database import database
from bp_test import example_blueprint

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # tutki mihin nämä siivotaan tästä

    database.init_app(app)

    app.register_blueprint(example_blueprint)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
