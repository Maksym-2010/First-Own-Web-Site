from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    name = StringField("Your name", validators=[DataRequired()])
    password = StringField("Text", validators=[DataRequired()])
    submit = SubmitField("Add comment")