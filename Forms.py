from wtforms import Form, StringField, EmailField, SubmitField, PasswordField, validators, BooleanField, DateField
from wtforms.validators import EqualTo, Length
from validate_email_address import validate_email

class Signup_Form(Form):
    username = StringField('Username',[validators.DataRequired(), Length(min=2)])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired(), Length(min=8)])
    confirmpass = PasswordField("Repeat Password", [validators.DataRequired(), Length(min=8), EqualTo('password', message="Passwords must match.")])
    submit = SubmitField('Sign Up')


class Login_Form(Form):
    username = StringField('Username',[validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])
    submit = SubmitField('Log In')

class CreateVoucherForm(Form):
    discount = StringField('Discount Percentage', [validators.Length(min=1, max=3), validators.DataRequired()])
    expiry_date = DateField('Expiry Date', format='%Y-%m-%d')
    points = StringField("Points Required", [validators.length(min=1, max=3), validators.DataRequired()])