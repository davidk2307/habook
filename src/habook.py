from flask import Flask
from flask import render_template,redirect
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import create_engine
from repository import DatabaseRepository
import forms
from loguru import logger

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

CATEGORIES = [{"name": "Haushalt"}, {"name": "Lebensmittel"}, {"name": "Gebäck"}]

@app.route("/")
def index():
    return redirect("/categories")

@app.route("/categories",methods=['GET','POST'])
def get_categories():
    form = forms.CategoryForm()
    if form.validate_on_submit():
        repository.create_category(form.name.data)
    categories = repository.get_categories()
    categories = [category[0] for category in categories]
    return render_template("categories.html", form=form, categories=categories)


@app.route('/category', methods=['GET','POST'])
def submit_category():
    form = forms.CategoryForm()
    if form.validate_on_submit():
        logger.info("test submit")
        return redirect('categories')
    return render_template('category.html', form=form)



app.run(debug=True)
