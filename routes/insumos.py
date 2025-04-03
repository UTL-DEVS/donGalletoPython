from flask import Blueprint, render_template, redirect, url_for, flash, request
from models.materiaPrima import MateriaPrima
from utils.db import db
from forms.form_insumo import InsumoForm

insumos_bp = Blueprint('insumos', __name__, url_prefix='/insumos', template_folder='templates')

UNIDADES = {
    1: "Gramos",
    2: "Mililitros",
    3: "Piezas",
    4: "Costal",
    5: "Litro",
    6: "Kilo",
    7: "Lata"
}

@insumos_bp.route('/insumos', methods=['GET', 'POST'])
def vista_admin_insumos():
    form = InsumoForm()
    form.unidad_medida.choices = list(UNIDADES.items())
    form.unidad_medida_publico.choices = list(UNIDADES.items())
    insumos = MateriaPrima.query.all()

    id_editar = request.args.get('editar')
    insumo_editar = MateriaPrima.query.get(id_editar) if id_editar else None

    if request.method == 'GET' and insumo_editar:
        form.id_materia.data = insumo_editar.id_materia
        form.nombre.data = insumo_editar.nombre_materia
        form.stock_materia.data = insumo_editar.stock_materia
        form.unidad_medida.data = insumo_editar.unidad_medida
        form.unidad_medida_publico.data = insumo_editar.unidad_medida_publico
        form.precio.data = insumo_editar.precio

    if form.validate_on_submit():
        nombre = form.nombre.data
        cantidad = float(form.stock_materia.data)
        unidad_base = form.unidad_medida.data
        unidad_publico = form.unidad_medida_publico.data
        precio = float(form.precio.data)

        # Conversión
        if unidad_base == 6:
            cantidad *= 1000
        elif unidad_base == 5:
            cantidad *= 1000
        elif unidad_base == 4:
            cantidad *= 1000 * 27

        if form.id_materia.data:
            insumo = MateriaPrima.query.get_or_404(int(form.id_materia.data))
            insumo.nombre_materia = nombre
            insumo.stock_materia = cantidad
            insumo.unidad_medida = unidad_base
            insumo.unidad_medida_publico = unidad_publico
            insumo.precio = precio
            flash("Insumo actualizado ✅", "success")
        else:
            nuevo = MateriaPrima(
                nombre_materia=nombre,
                stock_materia=cantidad,
                unidad_medida=unidad_base,
                unidad_medida_publico=unidad_publico,
                precio=precio,
                estatus=1
            )
            db.session.add(nuevo)
            flash("Insumo registrado ✅", "success")

        db.session.commit()
        return redirect(url_for('insumos.vista_admin_insumos'))

    return render_template('pages/page-insumo/admin.html',
                           form=form,
                           insumos=insumos,
                           unidades=UNIDADES)

@insumos_bp.route('/estatus/<int:id>')
def cambiar_estatus_insumo(id):
    insumo = MateriaPrima.query.get_or_404(id)
    insumo.estatus = 0 if insumo.estatus == 1 else 1
    db.session.commit()
    flash("Estatus del insumo actualizado ✅", "success")
    return redirect(url_for('insumos.vista_admin_insumos'))

@insumos_bp.route('/cocina')
def vista_cocina_insumos():
    insumos = MateriaPrima.query.filter_by(estatus=1).all()
    return render_template('pages/page-insumo/cocina.html', insumos=insumos, unidades=UNIDADES)
