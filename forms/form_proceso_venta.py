from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, HiddenField, RadioField
from wtforms.validators import DataRequired, NumberRange

class CarritoForm(FlaskForm):
    tipo_venta = StringField('Tipo Venta', validators=[DataRequired()])
    galleta_id = IntegerField('ID Galleta', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', default=1, validators=[NumberRange(min=1)])
    peso = IntegerField('Peso (gramos)', default=10, validators=[NumberRange(min=10)])
    tipo_paquete = RadioField('Tipo de Paquete', 
                            choices=[
                                ('100', 'Caja de 1kg (100 unidades)'),
                                ('70', 'Caja de 700g (70 unidades)'),
                                ('50', 'Media caja de 500g (50 unidades)')
                            ],
                            default='100')
    csrf_token = HiddenField()