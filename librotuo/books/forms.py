from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import IntegerField, DateField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    authors = StringField('Authors', validators=[DataRequired()])
    published_date = DateField('Published Date')
    ISBN_number = StringField('ISBN number')
    page_number = IntegerField('Pages number')
    cover_url = StringField('Address url to Book cover, like https://..')
    publication_language = StringField('publication language')
    submit = SubmitField('Add')
