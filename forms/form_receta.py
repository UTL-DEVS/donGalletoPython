from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, SelectField, SubmitField, StringField
from wtforms.validators import DataRequired
from models import MateriaPrima

class DetalleRecetaForm(FlaskForm):
    id_materia = SelectField('Materia Prima', coerce=int, validators=[DataRequired()])
    cantidad_insumo = FloatField('Cantidad por Materia Prima', validators=[DataRequired()])
    submit = SubmitField('Guardar Cambios')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_materia.choices = [(mp.id_materia, mp.nombre_materia) for mp in MateriaPrima.query.all()]
        


class RecetaForm(FlaskForm):
    nombre_receta = StringField('Nombre de la Receta', validators=[DataRequired()])
    id_galleta = SelectField('Galleta', coerce=int, validators=[DataRequired()])
    id_materia = SelectField('Materia Prima', coerce=int, validators=[DataRequired()])
    cantidad_insumo = FloatField('Cantidad por Materia Prima', validators=[DataRequired()])
    submit = SubmitField('Agregar Receta')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_materia.choices = [(mp.id_materia, mp.nombre_materia) for mp in MateriaPrima.query.all()]
        self.id_galleta.choices = [(g.id_galleta, g.nombre_galleta) for g in Galleta.query.filter_by(activo=True).all()]

