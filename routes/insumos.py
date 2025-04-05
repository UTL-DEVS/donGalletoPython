from utils import Blueprint, render_template, redirect, flash, db, url_for, request, login_required, current_user, abort
from models.materiaPrima import MateriaPrima
from models.proveedor import Proveedor
from utils.db import db
from forms.form_insumo import InsumoForm
from funcs import crear_log_user, crear_log_error

insumos_bp = Blueprint('insumos', __name__, url_prefix='/insumos', template_folder='templates')

UNIDADES = {
    1: "Gramos",
    2: "Costal",
    3: "Litro",
    4: "Kilo",
    5: "Lata"
}
UNIDADES_PUBLICAS = {
     1: "Gramos",
    3: "Litro",
    4: "Kilo",
}


def convertir_a_base(cantidad, unidad):
    conversiones = {
        1: 1,    
        3: 1000,   
        4: 1000,   
    }
    return cantidad * conversiones.get(unidad)

@insumos_bp.route('/insumo', methods=['GET', 'POST'])
@login_required
def vista_admin_insumos():
    if current_user.rol_user != 0:
        abort(404)
    crear_log_user(current_user.usuario, request.url)

    insumos = MateriaPrima.query.all()
    form = InsumoForm()
    form.unidad_medida.choices = list(UNIDADES.items())
    form.unidad_medida_publico.choices = list(UNIDADES_PUBLICAS.items())

    proveedores = Proveedor.query.all()
    form.id_proveedor.choices = [(p.id_proveedor, p.nombre_proveedor) for p in proveedores]

    if form.validate_on_submit():
        nombre = form.nombre.data
        cantidad = float(form.cantidad_compra.data)
        unidad_base = form.unidad_medida.data
        unidad_publico = form.unidad_medida_publico.data
        precio = float(form.precio.data)
        id_proveedor = form.id_proveedor.data
        cantidad_convertida = convertir_a_base(cantidad, unidad_publico)

        nuevo_insumo = MateriaPrima(
            nombre_materia=nombre,
            cantidad_compra=cantidad_convertida,
            unidad_medida=unidad_base,
            unidad_medida_publico=unidad_publico,
            precio=precio,
            estatus=1,
            id_proveedor=id_proveedor,
        )
        db.session.add(nuevo_insumo)
        db.session.commit()
        flash("✅ Insumo registrado correctamente", "success")
        return redirect(url_for('insumos.vista_admin_insumos'))

    return render_template('pages/page-insumo/admin.html', 
                        insumos=insumos, 
                        form=form, 
                        unidades=UNIDADES)


@insumos_bp.route('/insumo/editar/<int:id_materia>', methods=['GET', 'POST'])
@login_required
def editar_insumo(id_materia):
    if current_user.rol_user != 0:
        abort(404)
    crear_log_user(current_user.usuario, request.url)

    form = InsumoForm()
    form.unidad_medida.choices = list(UNIDADES.items())
    form.unidad_medida_publico.choices = list(UNIDADES_PUBLICAS.items())

    proveedores = Proveedor.query.all()
    form.id_proveedor.choices = [(p.id_proveedor, p.nombre_proveedor) for p in proveedores]
    inicial = 0
    
    insumo_editar = MateriaPrima.query.get_or_404(id_materia)
    if request.method == 'GET':
        if insumo_editar.unidad_medida_publico == 1:
            
            form.id_materia.data = insumo_editar.id_materia
            form.nombre.data = insumo_editar.nombre_materia
            form.cantidad_compra.data = insumo_editar.cantidad_compra
            form.unidad_medida.data = insumo_editar.unidad_medida
            form.unidad_medida_publico.data = insumo_editar.unidad_medida_publico
            form.precio.data = insumo_editar.precio
            form.id_proveedor.data = insumo_editar.id_proveedor
            inicial = form.cantidad_compra.data
        else:
            form.id_materia.data = insumo_editar.id_materia
            form.nombre.data = insumo_editar.nombre_materia
            form.cantidad_compra.data = insumo_editar.cantidad_compra / 1000
            form.unidad_medida.data = insumo_editar.unidad_medida
            form.unidad_medida_publico.data = insumo_editar.unidad_medida_publico
            form.precio.data = insumo_editar.precio
            form.id_proveedor.data = insumo_editar.id_proveedor
            inicial = form.cantidad_compra.data

    if form.validate_on_submit():
        nombre = form.nombre.data
        cantidad = float(form.cantidad_compra.data)
        unidad_base = form.unidad_medida.data
        unidad_publico = form.unidad_medida_publico.data
        precio = float(form.precio.data)
        id_proveedor = form.id_proveedor.data

        if insumo_editar.cantidad_compra != cantidad or insumo_editar.unidad_medida != unidad_base:
            cantidad_convertida = convertir_a_base(cantidad, unidad_publico)
        else:
            cantidad_convertida = cantidad


        insumo_editar.nombre_materia = nombre
        insumo_editar.cantidad_compra = cantidad_convertida
        insumo_editar.unidad_medida = unidad_base
        insumo_editar.unidad_medida_publico = unidad_publico
        insumo_editar.precio = precio
        insumo_editar.id_proveedor = id_proveedor

        db.session.commit()
        return redirect(url_for('insumos.vista_admin_insumos'))

    return render_template('pages/page-insumo/admin.html', form=form)

@insumos_bp.route('/estatus/<int:id>')
@login_required
def cambiar_estatus_insumo(id):
    if current_user.rol_user != 0:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)

        insumo = MateriaPrima.query.get_or_404(id)
        insumo.estatus = 0 if insumo.estatus == 1 else 1
        db.session.commit()
        flash("Estatus del insumo actualizado ✅", "success")
        return redirect(url_for('insumos.vista_admin_insumos'))

    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash("Error al cambiar estatus del insumo", "danger")
        return redirect('/error')

@insumos_bp.route('/cocina')
@login_required
def vista_cocina_insumos():
    if current_user.rol_user != 2:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)

        insumos = MateriaPrima.query.filter_by(estatus=1).all()
        return render_template('pages/page-insumo/cocina.html', insumos=insumos, unidades=UNIDADES)

    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash("Error al cargar insumos en cocina", "danger")
        return redirect('/error')