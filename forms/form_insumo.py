from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, HiddenField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class InsumoForm(FlaskForm):
    id_materia = IntegerField('id_materia',  widget={
        'type': 'hidden',
    })
    nombre = StringField('Nombre del insumo', validators=[DataRequired()])
    stock_materia = DecimalField('Cantidad', places=2, validators=[DataRequired(), NumberRange(min=0.0)], default=0.0)
    unidad_medida = SelectField('Unidad de medida (compra)', coerce=int, validators=[DataRequired(
        message='Debes escoger una opcion'
    )])
    unidad_medida_publico = SelectField('Unidad mostrada', coerce=int, validators=[DataRequired(
        message='Debes escoger una opcion'
    )])
    id_proveedor  = SelectField('Proveedores', coerce=int, validators=[DataRequired()])
    precio = DecimalField('Precio', places=2, validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar')
