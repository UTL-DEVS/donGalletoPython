from flask_wtf import FlaskForm
from wtforms import StringField, TelField
from wtforms.validators import DataRequired, length, number_range

class form_proveedor(FlaskForm):
    nombre_proveedor = StringField('Proveedor', [
        DataRequired('Ingrese el nombre de la empresa proveedora')
    ])
    