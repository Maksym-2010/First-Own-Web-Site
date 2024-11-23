from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo



class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=50)])
    phone = StringField("Phone Number", validators=[DataRequired(), Length(max=30)])
    email = StringField("Email", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo(
        "password", 
        message="Паролі мають співпадати!"
    )])
    submit = SubmitField("Register")