from flask_wtf import FlaskForm
from wtforms import StringField, TelField, EmailField
from wtforms.validators import DataRequired, length, number_range

class form_persona(FlaskForm):
    nombre = StringField('Nombre', [
        DataRequired('Ingrese el nombre!')
    ],render_kw={'class': 'nombrePersona'})

    primer_apellido = StringField('Primer apellido', [
        DataRequired('Ingrese su primer apellido!')
    ],render_kw={'class': 'primerApellidoPersona'})
    
    segundo_apellido = StringField('Segundo apellido', [
        DataRequired('Ingrese su segundo apellido!')
        ],render_kw={'class': 'segundoApellidoPersona'})
    
    correo = EmailField('Correo', [
        DataRequired('Ingrese su correo!')
    ],render_kw={'class': 'correoPersona'})
    
    direccion = StringField('Dirección', [
        DataRequired('Ingrese su dirección!')
    ],render_kw={'class': 'direccionPersona'})
    
    telefono = TelField('Telefóno', [
        DataRequired('Ingrese su número de teléfono')
    ],render_kw={'class': 'telefonoPersona'})