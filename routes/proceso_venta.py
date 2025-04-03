from flask import Blueprint, render_template, redirect, url_for, session, flash, send_from_directory, send_file
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

TICKETS_FOLDER = 'tickets'
os.makedirs(TICKETS_FOLDER, exist_ok=True)

venta_bp = Blueprint('venta', __name__, template_folder='templates')

@venta_bp.before_request
def antes_de_peticion():
    if 'carrito' not in session:
        session['carrito'] = []


@venta_bp.route('/ventas_dia')
def ventas_dia():
    ventas = ProcesoVentaDAO.obtener_ventas()
    return render_template('pages/pages-ventas/ventas_dia.html', ventas_dia=ventas)

@venta_bp.route('/tipo_venta')
def tipo_venta():
    return render_template('pages/pages-ventas/tipo_venta.html')

@venta_bp.route('/ventas/<tipo>')
def ventas(tipo):
    galletas = ProcesoVentaDAO.obtener_galletas_activas()
    carrito = session.get('carrito', [])
    total = sum(item.get('subtotal', 0) for item in carrito)
    
    return render_template('pages/pages-ventas/ventas.html', 
                         galletas=galletas, 
                         carrito=carrito, 
                         total=total,
                         tipo_venta=tipo)

@venta_bp.before_request
def antes_de_peticion():
    if 'carrito' not in session:
        session['carrito'] = []

@venta_bp.route('/agregar_al_carrito', methods=['POST'])
def agregar_al_carrito():
    form = CarritoForm()
    if form.validate_on_submit():
        try:
            tipo_venta = form.tipo_venta.data
            galleta_id = form.galleta_id.data
            galleta = ProcesoVentaDAO.obtener_galleta_por_id(galleta_id)
            
            if not galleta:
                flash('Galleta no encontrada', 'danger')
                return redirect(url_for('venta.ventas', tipo=tipo_venta))
            
            if tipo_venta == 'unidad':
                cantidad = int(form.cantidad.data)
                subtotal = galleta.precio_galleta * cantidad
                unidades = cantidad
            elif tipo_venta == 'peso':
                gramos = int(form.peso.data)
                unidades = gramos / 10 
                subtotal = galleta.precio_galleta * unidades
                cantidad = 1 
            elif tipo_venta == 'paquete':
                unidades = int(form.tipo_paquete.data)
                subtotal = galleta.precio_galleta * unidades
                cantidad = 1  
            
            valido, mensaje = ProcesoVentaCQRS.validar_item_carrito(galleta_id, unidades, tipo_venta)
            if not valido:
                flash(mensaje, 'danger')
                return redirect(url_for('venta.ventas', tipo=tipo_venta))
            
            item = {
                'galleta_id': galleta_id,
                'nombre': galleta.nombre_galleta,
                'precio_unitario': galleta.precio_galleta,
                'cantidad': cantidad,
                'subtotal': subtotal,
                'tipo_venta': tipo_venta,
                'unidades': unidades 
            }
            
            session['carrito'].append(item)
            session.modified = True
            flash('Producto agregado al carrito', 'success')
            
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        
        return redirect(url_for('venta.ventas', tipo=tipo_venta))
    
    return redirect(url_for('venta.tipo_venta'))


@venta_bp.route('/procesar_venta', methods=['POST'])
def procesar_venta():
    try:
        print("Iniciando procesamiento de venta")
        print("Contenido del carrito:", session.get('carrito'))
        
        if 'carrito' not in session or not session['carrito']:
            flash('El carrito está vacío', 'danger')
            return redirect(url_for('venta.ventas', tipo=session.get('tipo_venta_actual', 'unidad')))
        
        venta, ticket_path = ProcesoVentaController.procesar_venta(session)
        print(f"Venta procesada. ID: {venta.id}, Ticket: {ticket_path}")
        
        if not os.path.exists(ticket_path):
            raise Exception("No se pudo generar el ticket de venta")
        
        response = send_file(
            ticket_path,
            as_attachment=True,
            download_name=f"ticket_venta_{venta.id}.pdf",
            mimetype='application/pdf'
        )
        
        session.pop('carrito', None)
        session.modified = True
        
        return response
        
    except ValueError as e:
        print(f"Error de validación: {str(e)}")
        flash(str(e), 'danger')
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        flash(f'Error al procesar la venta: {str(e)}', 'danger')
        db.session.rollback()
    
    return redirect(url_for('venta.ventas', tipo=session.get('tipo_venta_actual', 'unidad')))

@venta_bp.route('/tickets/<int:venta_id>')
def descargar_ticket(venta_id):
    venta = ProcesoVentaDAO.obtener_venta_por_id(venta_id)
    if not venta:
        flash('Venta no encontrada', 'danger')
        return redirect(url_for('venta.listar_ventas'))
    
    filename = f"ticket_{venta_id}.pdf"
    filepath = os.path.join(controller_proceso_venta.TICKETS_FOLDER, filename)
    
    if not os.path.exists(filepath):
        controller_proceso_venta.generar_ticket(venta)
    
    return send_from_directory(controller_proceso_venta.TICKETS_FOLDER, filename, as_attachment=True)

@venta_bp.route('/listar_ventas')
def listar_ventas():
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
def vaciar_carrito():
    tipo_venta = session.get('tipo_venta_actual', 'unidad')
    session['carrito'] = []
    session.modified = True
    flash('Carrito vaciado correctamente', 'success')
    return redirect(url_for('venta.ventas', tipo=tipo_venta))

@venta_bp.route('/eliminar_item/<int:index>', methods=['POST'])
def eliminar_item(index):
    tipo_venta = session.get('tipo_venta_actual', 'unidad')
    try:
        session['carrito'].pop(index)
        session.modified = True
        flash('Item eliminado del carrito', 'success')
    except IndexError:
        flash('No se pudo eliminar el item', 'danger')
    return redirect(url_for('venta.ventas', tipo=tipo_venta))