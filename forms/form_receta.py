from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired
from models import MateriaPrima

class DetalleRecetaForm(FlaskForm):
    id_materia = SelectField('Materia Prima', coerce=int, validators=[DataRequired()])
    cantidad_insumo = FloatField('Cantidad por Materia Prima', validators=[DataRequired()])
    submit = SubmitField('Guardar Cambios')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_materia.choices = [(mp.id_materia, mp.nombre_materia) for mp in MateriaPrima.query.all()]
