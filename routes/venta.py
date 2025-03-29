from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash  
from datetime import datetime
from models.ventas import Producto
from forms.form_ventas import ProductoForm
from controller import controller_ventas
from controller import controller_resumen
from utils.db import db

venta_bp = Blueprint('venta', __name__, template_folder='templates')

@venta_bp.before_request
def antes_de_peticion():
    if 'carrito' not in session:
        session['carrito'] = []

@venta_bp.route('/ventas')
def ventas():
    productos = Producto.query.filter_by(activo=True).all()
    
    carrito = session.get('carrito', [])
    total = sum(item['subtotal'] for item in carrito)
    
    return render_template('pages/pages-ventas/ventas.html', 
                         galletas=productos, 
                         carrito=carrito, 
                         total=total)

@venta_bp.route('/api/agregar_carrito', methods=['POST'])
def agregar_carrito():
    datos = request.get_json()
    if not datos or 'producto_id' not in datos:
        return jsonify({'exito': False, 'error': 'Datos inválidos'}), 400
    
    try:
        producto_id = datos['producto_id']
        cantidad = int(datos['cantidad'])
        
        if cantidad < 1:
            return jsonify({'exito': False, 'error': 'La cantidad debe ser al menos 1'}), 400
            
        producto = Producto.query.get(producto_id)
        if not producto or not producto.activo:
            return jsonify({'exito': False, 'error': 'Producto no disponible'}), 404
        
        if cantidad > producto.cantidad:
            return jsonify({
                'exito': False,
                'error': f'Solo hay {producto.cantidad} unidades disponibles'
            }), 400
            
        carrito = session.get('carrito', [])
        item_existente = next((item for item in carrito if item['producto_id'] == producto_id), None)
        
        if item_existente:
            nueva_cantidad = item_existente['cantidad'] + cantidad
            if nueva_cantidad > producto.cantidad:
                return jsonify({
                    'exito': False,
                    'error': f'No puedes agregar {cantidad} más. Máximo disponible: {producto.cantidad - item_existente["cantidad"]}'
                }), 400
            
            item_existente['cantidad'] = nueva_cantidad
            item_existente['subtotal'] = nueva_cantidad * producto.precio
        else:
            carrito.append({
                'producto_id': producto.id,
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'cantidad': cantidad,
                'subtotal': float(producto.precio) * cantidad
            })
        
        session['carrito'] = carrito
        return jsonify({
            'exito': True,
            'carrito': carrito,
            'nuevo_total': sum(item['subtotal'] for item in carrito)
        })
        
    except (ValueError, TypeError):
        return jsonify({'exito': False, 'error': 'Cantidad inválida'}), 400

@venta_bp.route('/api/eliminar_del_carrito/<int:producto_id>', methods=['DELETE'])
def eliminar_del_carrito(producto_id):
    carrito = session.get('carrito', [])
    carrito = [item for item in carrito if item['producto_id'] != producto_id]
    session['carrito'] = carrito
    return jsonify({'exito': True, 'carrito': carrito})

@venta_bp.route('/api/vaciar_carrito', methods=['POST'])
def vaciar_carrito():
    session['carrito'] = []
    return jsonify({'exito': True})

@venta_bp.route('/api/procesar_venta', methods=['POST'])
def procesar_venta():
    carrito = session.get('carrito', [])
    if not carrito:
        return jsonify({'exito': False, 'error': 'El carrito está vacío'})
    
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'exito': False, 'error': 'Usuario no autenticado'})
    
    total = sum(item['subtotal'] for item in carrito)
    items = [{
        'producto_id': item['producto_id'],
        'cantidad': item['cantidad']
    } for item in carrito]
    
    resultado = controller_resumen.procesar_venta(total, usuario_id, items)
    
    if resultado:
        nombre_archivo = controller_resumen.generar_ticket(resultado)
        
        session['carrito'] = []
        
        return jsonify({
            'exito': True,
            'mensaje': 'Venta procesada con éxito',
            'url_ticket': f'/descargar_ticket/{resultado.id}'
        })
    else:
        return jsonify({'exito': False, 'error': 'Error al procesar la venta'})

@venta_bp.route('/api/corte_ventas', methods=['GET'])
def corte_ventas():
    reporte = controller_resumen.generar_reporte_diario()
    
    nombre_archivo = controller_resumen.generar_reporte_pdf(reporte)
    
    return jsonify({
        'exito': True,
        'reporte': reporte,
        'url_pdf': f'/descargar_reporte/{datetime.now().strftime("%Y%m%d")}'
    })

@venta_bp.route('/descargar_ticket/<int:venta_id>')
def descargar_ticket(venta_id):
    ticket_path = f"ticket_{venta_id}.pdf"
    return send_file(ticket_path, as_attachment=True)

@venta_bp.route('/descargar_reporte/<fecha>')
def descargar_reporte(fecha):
    reporte_path = f"corte_ventas_{fecha}.pdf"
    return send_file(reporte_path, as_attachment=True)

@venta_bp.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    form = ProductoForm()
    
    if form.validate_on_submit():
        imagen_file = request.files.get('imagen')
        
        producto_data = {
            'nombre': form.nombre.data.strip(),
            'precio': form.precio.data,
            'descripcion': form.descripcion.data.strip(),
            'cantidad': form.cantidad.data
        }
        
        producto = controller_ventas.agregar_producto(producto_data, imagen_file)
        
        if producto:
            flash('Producto agregado correctamente', 'success')
            return redirect(url_for('venta.ventas'))
        else:
            flash('Error: Verifica los datos del producto (nombre, precio, cantidad e imagen válida)', 'danger')
    
    return render_template('pages/pages-ventas/agregar_producto.html', form=form)

@venta_bp.route('/api/productos')
def api_productos():
    productos = controller_ventas.obtener_productos()
    productos_data = []
    
    for producto in productos:
        productos_data.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': producto.precio,
            'imagen': producto.imagen if producto.imagen else None,
            'descripcion': producto.descripcion,
            'cantidad': producto.cantidad
        })
    
    return jsonify(productos_data)