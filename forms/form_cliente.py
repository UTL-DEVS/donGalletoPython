from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, HiddenField, SubmitField, PasswordField
from wtforms.validators import DataRequired, NumberRange, EqualTo, Length

# Formulario para venta por paquetes (700g o 1kg)
class PaqueteForm(FlaskForm):
    id_galleta = HiddenField(validators=[DataRequired()])
    tipo_pedido = HiddenField(default="paquete")
    paquete = SelectField('Selecciona un paquete', choices=[(500, 'Paquete de 500g')], coerce=int, validators=[DataRequired()])
    cantidad = IntegerField('Cantidad de paquetes', default=1, validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Agregar al carrito')

# Formulario para venta por peso (g)
class PesoForm(FlaskForm):
    id_galleta = HiddenField(validators=[DataRequired()])
    tipo_pedido = HiddenField(default="peso")
    peso = SelectField('Selecciona el peso', choices=[(100, '100g'), (250, '250g'), (350, '350g')], coerce=int, validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', default=1, validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Agregar al carrito')

# Formulario para venta por piezas
class PiezaForm(FlaskForm):
    id_galleta = HiddenField(validators=[DataRequired()])
    tipo_pedido = HiddenField(default="pieza")
    cantidad = IntegerField('Cantidad de galletas', default=1, validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Agregar al carrito')

class CambioContrasenaForm(FlaskForm):
    contrasena_actual = PasswordField('Contraseña Actual', validators=[DataRequired()])
    nueva_contrasena = PasswordField('Nueva Contraseña', validators=[
        DataRequired(),
        Length(min=8, message="La contraseña debe tener al menos 8 caracteres."),
        EqualTo('confirmar_contrasena', message="Las contraseñas no coinciden.")
    ])
    confirmar_contrasena = PasswordField('Confirmar Nueva Contraseña', validators=[DataRequired()])
    submit = SubmitField('Cambiar Contraseña')