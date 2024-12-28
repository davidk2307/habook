from flask import Flask, Response
from flask import render_template, redirect
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import create_engine
from repository import DatabaseRepository
from model import BookingLine, Category
from datetime import date
import forms

# db = SQLAlchemy(model_class=Base)

engine = create_engine("sqlite:////Users/david/Documents/projects/habook/habook.db")
repository = DatabaseRepository(engine)

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
csrf = CSRFProtect(app)

# configure the database, relative to the app instance folder
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/david/Documents/projects/habook/habook.db"
# initialize the app with the extension
# db.init_app(app)


@app.route("/")
def index() -> Response:
    return redirect("/bookinglines")


@app.route("/categories", methods=["GET", "POST"])
def get_categories() -> str:
    form = forms.CategoryForm()
    if form.validate_on_submit():
        parent_id = None
        if form.parent_name.data is not None and form.parent_name.data != "":
            parent_id = int(form.parent_name.data)
        repository.create_category(form.name.data, parent_id=parent_id)
    categories = repository.get_categories()
    categories = [category[0] for category in categories]
    return render_template("categories.html", form=form, categories=categories)


@app.route("/bookinglines", methods=["GET", "POST"])
def get_booking_lines() -> str:
    booking_lines = [
        BookingLine(
            description="Gebäck",
            amount=-2.50,
            date=date(2024, 12, 28),
            category=Category(name="Lebensmittel"),
        ),
        BookingLine(
            description="Gehalt",
            amount=2234.50,
            date=date(2024, 12, 28),
            category=Category(name="Gehalt"),
        )
    ]
    return render_template("bookinglines.html", booking_lines=booking_lines)


app.run(debug=True)
