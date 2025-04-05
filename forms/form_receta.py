from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, SelectField, SubmitField, StringField
from wtforms.validators import DataRequired
from models import MateriaPrima, Galleta
class DetalleRecetaForm(FlaskForm):
    id_materia = SelectField('Materia Prima', coerce=int, validators=[DataRequired()])
    cantidad_insumo = FloatField('Cantidad por Materia Prima', validators=[DataRequired()])
    submit = SubmitField('Guardar Cambios')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Llenar las opciones del SelectField con el nombre de la materia prima y su unidad
        self.id_materia.choices = [
            (mp.id_materia, f"{mp.nombre_materia} ({self.obtener_unidad(mp.unidad_medida_publico)})") 
            for mp in MateriaPrima.query.all()
        ]

    def obtener_unidad(self, unidad_medida):
        # Método para obtener la unidad de medida en función del valor
        if unidad_medida == 1:
            return "gramos"
        elif unidad_medida == 3:
            return "litros"
        elif unidad_medida == 4:
            return "kilos"
        return "unidad desconocida"
 


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

