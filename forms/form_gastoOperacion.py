from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired

class GastoForm(FlaskForm):
    tipo = SelectField('Tipo de gasto', choices=[
        ('Agua', 'Agua'),
        ('Luz', 'Luz'),
        ('Internet y telefonía', 'Internet y telefonía'),
        ('Papelería', 'Papelería'),
        ('Transporte', 'Transporte'),
        ('Mantenimiento', 'Mantenimiento'),
        ('Compra de utensilios', 'Compra de utensilios'),
        ('Capacitación o asesoría', 'Capacitación o asesoría'),
        ('Gastos varios', 'Gastos varios')
    ], validators=[DataRequired()])

    monto = DecimalField('Monto', places=2, validators=[DataRequired()])
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Registrar gasto')
