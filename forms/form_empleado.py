from flask_wtf import FlaskForm
from wtforms import DecimalField,EmailField,SelectField,PasswordField,StringField,TelField
from wtforms.validators import DataRequired, length,  EqualTo, ValidationError
import re


class form_empleado(FlaskForm):
    #Persona
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

    # Empleado
    sueldo = DecimalField('Sueldo (al día)', [
        DataRequired('Ingrese el sueldo del empleado!'),
    ],render_kw={'id': 'sueldo'})
    dias_laborales = SelectField('Días de trabajo (a la semana)',[
        DataRequired('Ingrese el número de días que el empleado trabajará a la semana!')
    ],render_kw={'class': 'diasLaborales'}, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')])

    def validate_salario(self, field):
        if field.data <= 0:  # ✅ Mejor usar una comparación numérica
            raise ValidationError("El salario debe ser mayor a 0.")

    #Usuario
    nombre_usuario = StringField('Nombre de usuario', [
        DataRequired('Ingrese el nombre de usuario que desea')
    ],render_kw={'id': 'nombreUsuario'})

    rol_user = SelectField('Rol del usuario',[
        DataRequired('Ingrese su primer apellido!')
    ],render_kw={'class': 'rolUsuario'}, choices=[(0, 'Administrador'), (3, 'Cocinero'), (4, 'Vendedor')])
    
    correo = EmailField('Correo', [
        DataRequired('Ingrese su correo!')
    ],render_kw={'class': 'correoUsuario'})
    
    contrasenia = PasswordField('Contraseña', [
        DataRequired('Ingrese su contraseña!')
    ], render_kw={'class': 'contraseniaUsuario'})

    confirmar_contrasenia = PasswordField('Confirmar contraseña', [
        DataRequired('Confirme su contraseña!'),
        EqualTo('contrasenia', message='Las contraseñas no coinciden.')
    ], render_kw={'class': 'contraseniaUsuario'})

    def validate_contrasenia(self, field):
        """
        Verifica que la contraseña cumpla con:
        - Al menos 8 caracteres
        - Al menos una letra mayúscula
        - Al menos una letra minúscula
        - Al menos un número
        - Al menos un carácter especial (!@#$%^&*(), etc.)
        """
        password = field.data
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            raise ValidationError(
                'Contraseña incorrecta. Debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial.'
            )