from flask_wtf import FlaskForm
from wtforms import HiddenField
from wtforms.validators import DataRequired

class CarritoForm(FlaskForm):
    galleta_id = HiddenField(validators=[DataRequired()])
    cantidad = HiddenField(validators=[DataRequired()])