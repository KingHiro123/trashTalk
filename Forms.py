from wtforms import Form, StringField, EmailField, SubmitField, PasswordField, validators, BooleanField, ValidationError
from wtforms.validators import EqualTo, Length
from validate_email_address import validate_email

class Signup_Form(Form):
    username = StringField('Username',[validators.DataRequired(), Length(min=2)])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired(), Length(min=8)])
    confirmpass = PasswordField("Repeat Password", [validators.DataRequired(), EqualTo('password', message="Passwords must match."), Length(min=8)  ])
    submit = SubmitField('Sign Up')


class Login_Form(Form):
    username = StringField('Username',[validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')