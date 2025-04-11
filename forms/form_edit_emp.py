from flask_wtf import FlaskForm
from wtforms import DecimalField,EmailField,SelectField,StringField,TelField
from wtforms.validators import DataRequired, length,  EqualTo, ValidationError


class form_edit_emp (FlaskForm):
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
    dias_laborales = SelectField('Días de trabajo (a la quincena)',[
        DataRequired('Ingrese el número de días que el empleado trabajará a la quincena!')
    ],render_kw={'class': 'diasLaborales'}, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'),
                                                (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15')])

    def validate_salario(self, field):
        if field.data <= 0:  # ✅ Mejor usar una comparación numérica
            raise ValidationError("El salario debe ser mayor a 0.")
