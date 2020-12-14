from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, \
                    TextAreaField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Email, InputRequired, Length
from wtforms import ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from .models import CustomerUser

class CustomerRegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired('Name is required')])
    username = StringField('Username', validators=[InputRequired('Username is required'),
        Length(min=5, max=15, message="Username must be in between 5 and 15 ")])
    email = StringField('Email', validators=[InputRequired('Email is required'), Email('Invalid Email')])
    password = PasswordField('Password', validators=[InputRequired('Password is required'),
                                 EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm')
    country = StringField('Country', validators=[InputRequired('Country is required')])
    state = StringField('State', validators=[InputRequired('State is required')])
    city  = StringField('City', validators=[InputRequired('City is required')])
    contact = StringField('Contact', validators=[InputRequired('Contact is required')])
    address = StringField('Address', validators=[InputRequired('Address is required')])
    zipcode = StringField('Zip code', validators=[InputRequired('Zip code is required')])
    profile = FileField('Profile', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], "Images Only Please")])
    submit = SubmitField('Register')

    #checking the username
    def validate_username(self, field):
        user = CustomerUser.query.filter_by(username=field.data).first()
        if user :
            raise ValidationError('Username already in use.')

    #checking the email id
    def validate_email(self, field):
        user = CustomerUser.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Email already registered.')

    def validate_contact(self, field):
        if len(field.data) != 10:
            raise ValidationError('You have entered wrong number')



class CustomerLoginForm(FlaskForm):
    name = StringField()
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')
