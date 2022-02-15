from wtforms import Form, StringField, DateField, validators


class AddItemForm(Form):
    datemanufactured = DateField('Date of Manufacture', [
        validators.DataRequired()], format='%Y-%m-%d')
    remarks = StringField('Remarks', [
        validators.Length(min=1, max=50), validators.DataRequired()])
