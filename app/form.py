from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length

class SearchForm(FlaskForm):
    search = StringField('Поиск:', validators=[Length(0, 64)])
    submit = SubmitField('Искать')