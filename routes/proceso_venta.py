from flask import Blueprint, render_template, redirect, url_for, session, flash, send_from_directory, send_file, request
from controller import controller_proceso_venta, ProcesoVentaController
from dao.dao_proceso_venta import ProcesoVentaDAO
from models.Stock import Stock
from models.galleta import Galleta
from models.ProcesoVenta import ProcesoVenta, DetalleVenta
from cqrs.cqrs_proceso_venta import ProcesoVentaCQRS
from forms.form_proceso_venta import CarritoForm
from utils import db
import os
import datetime
from funcs.pdf import generar_pdf_venta
from utils import login_required, current_user, abort

TICKETS_FOLDER = 'tickets'
os.makedirs(TICKETS_FOLDER, exist_ok=True)

venta_bp = Blueprint('venta', __name__, template_folder='templates')

@venta_bp.before_request
def antes_de_peticion():
    if 'carrito' not in session:
        session['carrito'] = []


@venta_bp.route('/ventas_dia')
@login_required
def ventas_dia():
    if current_user.rol_user != 4:
        abort(404)
    ventas = ProcesoVentaDAO.obtener_ventas()
    return render_template('pages/pages-ventas/ventas_dia.html', ventas_dia=ventas)

@venta_bp.route('/tipo_venta')
@login_required
def tipo_venta():
    print(current_user.rol_user)
    if current_user.rol_user != 4:
        abort(404)
    return render_template('pages/pages-ventas/tipo_venta.html')

@venta_bp.route('/ventas/<tipo>')
@login_required
def ventas(tipo):
    if current_user.rol_user != 4:
        abort(404)
    galletas = ProcesoVentaDAO.obtener_galletas_activas()
    carrito = session.get('carrito', [])
    total = sum(item.get('subtotal', 0) for item in carrito)
    
    return render_template('pages/pages-ventas/ventas.html', 
                         galletas=galletas, 
                         carrito=carrito, 
                         total=total,
                         tipo_venta=tipo)

@venta_bp.route('/agregar_al_carrito', methods=['POST'])
@login_required
def agregar_al_carrito():
    if current_user.rol_user != 4:
        abort(404)
    form = CarritoForm()
    if form.validate_on_submit():
        try:
            tipo_venta = form.tipo_venta.data
            galleta_id = form.galleta_id.data
            galleta = ProcesoVentaDAO.obtener_galleta_por_id(galleta_id)
            
            if not galleta:
                flash('Galleta no encontrada', 'danger')
                return redirect(url_for('venta.ventas', tipo=tipo_venta))
            
            stock = Stock.query.filter_by(id_galleta=galleta_id).first()
            if not stock:
                flash('No hay stock disponible para esta galleta', 'danger')
                return redirect(url_for('venta.ventas', tipo=tipo_venta))
            
            if tipo_venta == 'unidad':
                cantidad = int(form.cantidad.data)
                unidades_equivalentes = cantidad
                metadata = {'cantidad_unidades': cantidad, 'gramos': 0, 'cantidad_paquetes': 0}
            elif tipo_venta == 'peso':
                gramos = int(form.peso.data)
                unidades_equivalentes = gramos / 10
                metadata = {'cantidad_unidades': 0, 'gramos': gramos, 'cantidad_paquetes': 0}
            elif tipo_venta == 'paquete':
                unidades_por_paquete = int(form.tipo_paquete.data)
                unidades_equivalentes = unidades_por_paquete
                metadata = {'cantidad_unidades': 0, 'gramos': 0, 'cantidad_paquetes': 1}
            
            if stock.cantidad_galleta < unidades_equivalentes:
                flash(f'Stock insuficiente. Disponibles: {stock.cantidad_galleta} unidades equivalentes', 'danger')
                return redirect(url_for('venta.ventas', tipo=tipo_venta))
            
            subtotal = galleta.precio_galleta * unidades_equivalentes
            
            carrito = session.get('carrito', [])
            item_existente = next(
                (item for item in carrito 
                 if item['galleta_id'] == galleta_id and item['tipo_venta'] == tipo_venta),
                None
            )
            
            if item_existente:
                if tipo_venta == 'unidad':
                    item_existente['cantidad'] += cantidad
                elif tipo_venta == 'peso':
                    item_existente['gramos'] += gramos
                elif tipo_venta == 'paquete':
                    item_existente['cantidad_paquetes'] += 1
                
                item_existente['unidades_equivalentes'] += unidades_equivalentes
                item_existente['subtotal'] += subtotal
                item_existente['metadata_json'] = metadata
            else:
                nuevo_item = {
                    'galleta_id': galleta_id,
                    'nombre': galleta.nombre_galleta,
                    'precio_unitario': galleta.precio_galleta,
                    'tipo_venta': tipo_venta,
                    'subtotal': subtotal,
                    'unidades_equivalentes': unidades_equivalentes,
                    'metadata_json': metadata
                }
                
                if tipo_venta == 'unidad':
                    nuevo_item['cantidad'] = cantidad
                elif tipo_venta == 'peso':
                    nuevo_item['gramos'] = gramos
                elif tipo_venta == 'paquete':
                    nuevo_item['cantidad_paquetes'] = 1
                
                carrito.append(nuevo_item)
            
            session['carrito'] = carrito
            session.modified = True
            flash('Producto agregado al carrito', 'success')
            
        except ValueError as e:
            flash(f'Error en los datos: {str(e)}', 'danger')
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'danger')
        
        return redirect(url_for('venta.ventas', tipo=tipo_venta))
    
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Error en {getattr(form, field).label.text}: {error}', 'danger')
    return redirect(url_for('venta.ventas', tipo=form.tipo_venta.data if form.tipo_venta.data else 'unidad'))

@venta_bp.route('/procesar_venta', methods=['POST'])
@login_required
def procesar_venta():
    if current_user.rol_user != 4:
        abort(404)
    
    if 'carrito' not in session or not session['carrito']:
        flash('El carrito está vacío', 'danger')
        return redirect(url_for('venta.ventas', tipo=session.get('tipo_venta_actual', 'unidad')))
    
    try:
        for item in session['carrito']:
            stock = Stock.query.filter_by(id_galleta=item['galleta_id']).first()
            unidades = item.get('unidades_equivalentes', item.get('cantidad', 0))
            if not stock or stock.cantidad_galleta < unidades:
                flash(f'Stock insuficiente para {item["nombre"]}', 'danger')
                return redirect(url_for('venta.ventas', tipo=session.get('tipo_venta_actual', 'unidad')))
        
        venta, ticket_path = ProcesoVentaController.procesar_venta(session)
        
        if not os.path.exists(ticket_path):
            flash('Error al generar el ticket', 'danger')
            return redirect(url_for('venta.ventas', tipo=session.get('tipo_venta_actual', 'unidad')))
        
        session.pop('carrito', None)
        session.modified = True
        
        return send_file(
            ticket_path,
            as_attachment=True,
            download_name=f"ticket_venta_{venta.id}.pdf",
            mimetype='application/pdf'
        )
        
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash(f'Error al procesar la venta: {str(e)}', 'danger')
        db.session.rollback()
    
    return redirect(url_for('venta.ventas', tipo=session.get('tipo_venta_actual', 'unidad')))

@venta_bp.route('/tickets/<int:venta_id>')
@login_required
def descargar_ticket(venta_id):
    if current_user.rol_user != 4:
        abort(404)
    venta = ProcesoVentaDAO.obtener_venta_por_id(venta_id)
    if not venta:
        flash('Venta no encontrada', 'danger')
        return redirect(url_for('venta.listar_ventas'))
    
    filename = f"ticket_{venta_id}.pdf"
    filepath = os.path.join(controller_proceso_venta.TICKETS_FOLDER, filename)
    
    if not os.path.exists(filepath):
        controller_proceso_venta.generar_ticket(venta)
    
    if request.args.get('view') == '1':
        return send_from_directory(controller_proceso_venta.TICKETS_FOLDER, filename, as_attachment=False)
    
    return send_from_directory(controller_proceso_venta.TICKETS_FOLDER, filename, as_attachment=True)

@venta_bp.route('/listar_ventas')
@login_required
def listar_ventas():
    if current_user.rol_user != 0:
        abort(404)
        
    ventas = ProcesoVentaDAO.obtener_ventas()
    return render_template('pages/pages-ventas/cancelar_venta.html', lista_ventas=ventas)

@venta_bp.route('/eliminar_venta/<int:venta_id>', methods=['POST'])
def eliminar_venta(venta_id):
    if ProcesoVentaDAO.eliminar_venta(venta_id):
        flash('Venta cancelada correctamente', 'success')
    else:
        flash('No se pudo cancelar la venta', 'danger')
    return redirect(url_for('venta.listar_ventas'))

@venta_bp.route('/vaciar_carrito', methods=['POST'])
@login_required
def vaciar_carrito():
    tipo_venta = session.get('tipo_venta_actual', 'unidad')
    session['carrito'] = []
    session.modified = True
    flash('Carrito vaciado correctamente', 'success')
    return redirect(url_for('venta.ventas', tipo=tipo_venta))

@venta_bp.route('/eliminar_item/<int:index>', methods=['POST'])
@login_required
def eliminar_item(index):
    tipo_venta = session.get('tipo_venta_actual', 'unidad')
    try:
        session['carrito'].pop(index)
        session.modified = True
        flash('Item eliminado del carrito', 'success')
    except IndexError:
        flash('No se pudo eliminar el item', 'danger')
    return redirect(url_for('venta.ventas', tipo=tipo_venta))