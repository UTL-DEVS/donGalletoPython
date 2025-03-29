from flask_wtf import FlaskForm
from wtforms import HiddenField
from wtforms.validators import DataRequired

class CarritoForm(FlaskForm):
    producto_id = HiddenField(validators=[DataRequired()])
    cantidad = HiddenField(validators=[DataRequired()])