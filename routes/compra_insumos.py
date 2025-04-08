from utils import Blueprint, render_template, redirect, request, login_required, current_user, flash, url_for, abort, db
from models import CompraInsumo as Compra, Persona,Usuario, DetalleCompraInsumo as Detalles, MateriaPrima
from forms import form_empleado
compra_insumo_admin_bp = Blueprint('compra_admin', __name__, url_prefix='/compraAdmin', template_folder='templates')

@compra_insumo_admin_bp.route('/', methods=['GET'])
@login_required
def mostrar_compras():
    form = form_empleado()
    #compras_pendientes = Compra.query.filter_by(estatus=0).all()
    compras_pendientes = obtener_compras_con_usuarios()
    return render_template('pages/page-admin/compras.html', compras=compras_pendientes, f=form)

@compra_insumo_admin_bp.route('/compras/aceptar', methods=['POST'])
@login_required
def aceptar_compra():
    compra = Compra.query.get_or_404((request.args.get('id_compra')))
    if compra.estatus == 1:
        flash('Esta compra ya fue aceptada.', 'warning')
        return redirect('/compraAdmin')

    for detalle in compra.detalles:
        materia = detalle.materia_prima
<<<<<<< HEAD
        print(f'Se suma {materia.stock_materia} mas {detalle.cantidad}')
        materia.stock_materia += detalle.cantidad
        
=======
        cantidadAgregar = materia.cantidad_compra * detalle.cantidad
        print('por agregar')
        print(cantidadAgregar)
        print('stock actual')
        print(materia.stock_materia)
        materia.stock_materia += cantidadAgregar
        print('actualizado')
        print(materia.stock_materia)

>>>>>>> 2e1d6bbef67ecdb4de7ecb87308fd9ef37922fbe
    compra.estatus = 1  # Marcar como aceptada
    db.session.commit()
    flash('Compra aceptada y stock actualizado.', 'success')
    return redirect('/compraAdmin')

def obtener_compras_con_usuarios():
    compras = db.session.query(Compra).join(Usuario).join(Persona).with_entities(
        Compra.id_compra_insumo,
        Compra.fecha_compra,
        Compra.total,
        Compra.estatus,
        Persona.nombre,
        Persona.primerApellido,
        Persona.segundoApellido 
    ).all()

    return compras

@compra_insumo_admin_bp.route('/detalleCompra', methods=['POST'])
@login_required
def ver_detalles_compra():
    form = form_empleado()
    id_compra= request.args.get('id_comp')
    print(f'id: {id_compra}')
    compra = db.session.query(Compra).filter(Compra.id_compra_insumo ==id_compra).first()
    detalles = db.session.query(Detalles).filter(Detalles.id_compra==id_compra).join(MateriaPrima).all()
    print(f'detalles {detalles}')
    compras_pendientes = obtener_compras_con_usuarios()
    return render_template('pages/page-admin/compras.html', compras=compras_pendientes, f=form, compra=compra, detalles=detalles, modal='true')