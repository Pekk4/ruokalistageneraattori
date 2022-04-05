from flask import Flask
from config import DATABASE_URL, SECRET_KEY
from database import database
from blueprints.index import index_blueprint
from blueprints.login import login_blueprint
from blueprints.register import register_blueprint

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # tutki mihin nämä siivotaan tästä
    app.secret_key = SECRET_KEY


    database.init_app(app)

    app.register_blueprint(index_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(register_blueprint)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port="5000")
