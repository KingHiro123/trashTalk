from wtforms import Form, StringField, IntegerField, validators, SubmitField


class AddFieldForm(Form):
    item_brand = StringField('Item Brand', [validators.Length(
        min=1, max=30), validators.DataRequired()])
    item_description = StringField('Item Description', [
                                   validators.Length(min=1, max=50), validators.DataRequired()])
    submit = SubmitField('Update')
