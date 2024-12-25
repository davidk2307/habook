from flask import Flask
from flask import render_template
from sqlalchemy import create_engine
from repository import DatabaseRepository

# db = SQLAlchemy(model_class=Base)

engine = create_engine("sqlite:////Users/david/Documents/projects/habook/habook.db")
repository = DatabaseRepository(engine)

app = Flask(__name__)

# configure the database, relative to the app instance folder
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/david/Documents/projects/habook/habook.db"
# initialize the app with the extension
# db.init_app(app)

CATEGORIES = [{"name": "Haushalt"}, {"name": "Lebensmittel"}, {"name": "Gebäck"}]


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/categories")
def get_categories():
    categories = repository.get_categories()
    categories = [category[0] for category in categories]
    return render_template("categories.html", categories=categories)


app.run(debug=True)
