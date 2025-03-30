from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, IntegerField, HiddenField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from wtforms.fields import DateField

class GalletaForm(FlaskForm):
    galleta_id = HiddenField(validators=[DataRequired()])
    cantidad = IntegerField("Cantidad", validators=[DataRequired(), NumberRange(min=1)])

class PedidoForm(FlaskForm):
    galletas = FieldList(FormField(GalletaForm))
    fecha_recoleccion = DateField("Fecha de recolección", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField("Enviar Pedido")
