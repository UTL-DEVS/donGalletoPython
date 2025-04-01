from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, EmailField,PasswordField
from wtforms.validators import DataRequired, length, number_range

class form_empleado(FlaskForm):
    nombre_usuario = StringField('Sueldo', [
        DataRequired('Ingrese el sueldo del empleado!')
    ],render_kw={'id': 'nombreUsuario'})
