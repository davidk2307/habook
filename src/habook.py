from flask import Flask
from flask import flash
from flask import render_template, redirect
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import create_engine
from repository import DatabaseRepository
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
def index():
    return redirect("/categories")


@app.route("/categories", methods=["GET", "POST"])
def get_categories():
    form = forms.CategoryForm()
    if form.validate_on_submit():
        parent_id = None
        if form.parent_name.data is not None and form.parent_name.data != "":
            parent_id = int(form.parent_name.data)
        repository.create_category(form.name.data, parent_id=parent_id)
    categories = repository.get_categories()
    categories = [category[0] for category in categories]
    return render_template("categories.html", form=form, categories=categories)


app.run(debug=True)
