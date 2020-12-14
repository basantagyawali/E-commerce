from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, \
                    TextAreaField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Email, InputRequired, Length
from wtforms import ValidationError


class LoginForm(FlaskForm):
    name = StringField()
    email = StringField('Email')
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')
