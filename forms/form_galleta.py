from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, FileField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class GalletaForm(FlaskForm):
    nombre_galleta = StringField('Nombre', validators=[DataRequired()])
    precio_galleta = FloatField('Precio', validators=[DataRequired(), NumberRange(min=1.0)])
    descripcion_galleta = TextAreaField('Descripción')
    imagen_galleta = FileField('Imagen de la Galleta')
    cantidad_galleta = IntegerField('Cantidad inicial', validators=[NumberRange(min=0)], default=0)