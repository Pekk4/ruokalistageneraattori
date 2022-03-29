from flask import Flask
#from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

from flask import *

from repositories.repository import Repository


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
repo = Repository(db)


@app.route("/")
def index():
    meals = repo.find_all_meals()

    return render_template("index.html", meals=meals) 


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
