from flask_wtf import FlaskForm
from wtforms import StringField, TelField
from wtforms.validators import DataRequired, length, number_range

class login_form(FlaskForm):
    nombre_proveedor = StringField('nombre del proveedor', [
        DataRequired('Ingrese el nombre del proveedor')
    ])
    telefono = TelField('Telefóno')