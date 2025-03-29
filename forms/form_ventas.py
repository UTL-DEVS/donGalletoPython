from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, FileField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    precio = FloatField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    descripcion = TextAreaField('Descripción')
    imagen = FileField('Imagen del Producto')
    cantidad = IntegerField('Cantidad inicial', validators=[NumberRange(min=0)], default=0)