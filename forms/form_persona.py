from flask_wtf import FlaskForm
from wtforms import StringField, TelField, EmailField
from wtforms.validators import DataRequired, length, number_range

class form_persona(FlaskForm):
    nombre = StringField('Nombre', [
        DataRequired('Ingrese el nombre!')
    ])
    apellido = StringField('Apellidos', [
        DataRequired('Ingrese el nombre!')
    ])
    correo = EmailField('Correo', [
        DataRequired('Ingrese el nombre!')
    ])
    direccion = StringField('Dirección', [
        DataRequired('Ingrese el nombre!')
    ])
    telefono = TelField('Telefóno')