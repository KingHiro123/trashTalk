from wtforms import Form, StringField, TextAreaField, validators
from Base import *
from datetime import datetime


class CreateFaqForm (Form):
    question = StringField('Question', [validators.Length(min=1, max=150), validators.DataRequired()])
    answer = TextAreaField(('Answer', [validators.Length(min=1, max=500), validators.DataRequired()]))


class CreateFeedbackForm (Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    subject = StringField('Subject', [validators.Length(min=1, max=150), validators.DataRequired()])
    content = TextAreaField('Content', [validators.Length(min=1, max=5000), validators.DataRequired()])
