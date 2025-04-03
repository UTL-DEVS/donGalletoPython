from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, HiddenField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class InsumoForm(FlaskForm):
    id_materia = HiddenField()
    nombre = StringField('Nombre del insumo', validators=[DataRequired()])
    stock_materia = DecimalField('Cantidad', places=2, validators=[DataRequired(), NumberRange(min=0.01)])
    unidad_medida = SelectField('Unidad de medida (real)', coerce=int, validators=[DataRequired()])
    unidad_medida_publico = SelectField('Unidad mostrada al público', coerce=int, validators=[DataRequired()])
    precio = DecimalField('Precio', places=2, validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar')
