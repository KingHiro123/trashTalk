from wtforms import Form, StringField, EmailField, SubmitField, PasswordField, validators, ValidationError
from wtforms.validators import EqualTo, Length
from validate_email_address import validate_email

class Signup_Form(Form):
    username = StringField('Username',[validators.DataRequired(), Length(min=2)])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])
    confirmpass = PasswordField("Repeat Password", [validators.DataRequired(), EqualTo('password', message="Passwords must match.")])
    submit = SubmitField('Sign Up')


class Login_Form(Form):
    username = StringField('Username',[validators.DataRequired(), Length(min=2)])
    password = PasswordField("Password", [validators.DataRequired()])
    submit = SubmitField('Log In')