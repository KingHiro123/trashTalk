from wtforms import Form, StringField, DateField, validators

class CreateVoucherForm(Form):
    discount = StringField('Discount Percentage', [validators.Length(min=1, max=3), validators.DataRequired()])
    expiry_date = DateField('Expiry Date', format='%Y-%m-%d')
    points = StringField("Points Required", [validators.length(min=1, max=3), validators.DataRequired()])