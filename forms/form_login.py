from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, IntegerField
from wtforms.validators import DataRequired, length, number_range

class login_form(FlaskForm):
    usuario = StringField('usuario', [
        DataRequired('Usuario vacio')
    ])
    contrasenia = PasswordField('contrasenia', [
        DataRequired('Contrasenia necesaria'),
        length(min=8, message='La contraseña debe tener minimo 8 caracteres') 
    ])
    captcha = StringField('Captcha', [
        DataRequired('Captcha necesario'),
        length(min=5, max=5, message='Caracteres fuere del rango')
    ])