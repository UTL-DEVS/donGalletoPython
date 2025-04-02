from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, EmailField,PasswordField
from wtforms.validators import DataRequired, length, number_range

class form_usuario(FlaskForm):
    nombre_usuario = StringField('Nombre de usuario', [
        DataRequired('Ingrese el nombre de usuario que desea')
    ],render_kw={'id': 'nombreUsuario'})

    rol_user = SelectField('Rol del usuario',[
        DataRequired('Ingrese su primer apellido!')
    ],render_kw={'class': 'rolUsuario'}, choices=[(0, 'Administrador'), (1, 'Cliente'), (2, 'Cocinero'), (3, 'Vendedor')])
    
    correo = EmailField('Correo', [
        DataRequired('Ingrese su correo!')
    ],render_kw={'class': 'correoUsuario'})
    
    contrasenia = PasswordField('Contraseña', [
        DataRequired('Ingrese su contraseña!')
    ],render_kw={'class': 'contraseniaUsuario'})
