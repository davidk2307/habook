from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CategoryForm(FlaskForm):
    name = StringField(
        "name",
        default="",
        validators=[
            DataRequired(),
            Length(
                max=50, message="Name der Kategorie darf maximal 50 Zeichen lang sein"
            ),
        ],
    )
