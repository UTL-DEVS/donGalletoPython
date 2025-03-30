from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash, send_file
from datetime import datetime
from models import Producto
from forms.form_ventas import ProductoForm
from controller import controller_ventas
from controller import controller_resumen
from utils.db import db
from cqrs import cqrs_resumen, cqrs_ventas
from flask_wtf.csrf import validate_csrf


venta_bp = Blueprint('venta', __name__, template_folder='templates')

@venta_bp.route('/tipo_venta')
def tipo_venta():
    return render_template('pages/pages-ventas/tipo_venta.html')

@venta_bp.before_request
def antes_de_peticion():
    if 'carrito' not in session:
        session['carrito'] = []

@venta_bp.route('/ventas')
def ventas():
    tipo_venta = request.args.get('tipo', 'unidad')
    productos = Producto.query.filter_by(activo=True).all()
    
    carrito = session.get('carrito', [])
    total = sum(item['subtotal'] for item in carrito)
    
    return render_template('pages/pages-ventas/ventas.html', 
                         galletas=productos, 
                         carrito=carrito, 
                         total=total,
                         tipo_venta=tipo_venta)



@venta_bp.route('/api/agregar_carrito', methods=['POST'])
def agregar_carrito():
    try:
        validate_csrf(request.headers.get('X-CSRFToken'))
        if not request.is_json:
            return jsonify({
                'exito': False,
                'error': 'Se esperaba JSON'
            }), 400

        datos = request.get_json()
        
        campos_requeridos = ['producto_id', 'cantidad', 'producto_nombre', 'precio', 'tipo_venta']
        for campo in campos_requeridos:
            if campo not in datos:
                return jsonify({
                    'exito': False,
                    'error': f'Falta el campo requerido: {campo}'
                }), 400

        try:
            producto_id = int(datos['producto_id'])
            cantidad = int(datos['cantidad'])
            precio = float(datos['precio'])
            unidades = int(datos.get('unidades', cantidad))
            producto_nombre = str(datos['producto_nombre'])
            tipo_venta = str(datos['tipo_venta'])
        except (ValueError, TypeError) as e:
            return jsonify({
                'exito': False,
                'error': 'Tipos de datos inválidos'
            }), 400

        carrito = session.get('carrito', [])
        
        item_existente = next(
            (item for item in carrito 
             if (item['producto_id'] == producto_id and 
                 item['nombre'] == producto_nombre and
                 item.get('tipo_venta') == tipo_venta)), 
            None
        )
        
        if item_existente:
            if tipo_venta == 'unidad':
                item_existente['cantidad'] += cantidad
                item_existente['subtotal'] = item_existente['cantidad'] * (item_existente['precio'] / item_existente['cantidad'])
            else: 
                item_existente['unidades'] += unidades
                item_existente['subtotal'] += precio
        else:
            nuevo_item = {
                'producto_id': producto_id,
                'nombre': producto_nombre,
                'precio': precio,
                'cantidad': cantidad,
                'unidades': unidades,
                'subtotal': precio,
                'tipo_venta': tipo_venta
            }
            carrito.append(nuevo_item)
        
        session['carrito'] = carrito
        session.modified = True
        
        return jsonify({
            'exito': True,
            'carrito': carrito,
            'nuevo_total': sum(item['subtotal'] for item in carrito),
            'mensaje': 'Producto agregado al carrito'
        })
        
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': str(e)
        }), 500

@venta_bp.route('/api/eliminar_del_carrito/<int:producto_id>', methods=['DELETE'])
def eliminar_del_carrito(producto_id):
    try:
        data = request.get_json()
        producto_nombre = data.get('producto_nombre')
        tipo_venta = data.get('tipo_venta')
        
        if not producto_nombre or not tipo_venta:
            return jsonify({
                'exito': False,
                'error': 'Faltan datos para identificar el producto'
            }), 400
        
        carrito = session.get('carrito', [])
        nuevo_carrito = [
            item for item in carrito 
            if not (item['producto_id'] == producto_id and 
                   item['nombre'] == producto_nombre and
                   item.get('tipo_venta') == tipo_venta)
        ]
        
        session['carrito'] = nuevo_carrito
        session.modified = True
        
        return jsonify({
            'exito': True,
            'carrito': nuevo_carrito,
            'nuevo_total': sum(item['subtotal'] for item in nuevo_carrito)
        })
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': str(e)
        }), 500

@venta_bp.route('/api/vaciar_carrito', methods=['POST'])
def vaciar_carrito():
    try:
        session['carrito'] = []
        session.modified = True
        return jsonify({
            'exito': True,
            'mensaje': 'Carrito vaciado correctamente'
        })
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': str(e)
        }), 500

@venta_bp.route('/api/procesar_venta', methods=['POST'])
def procesar_venta():
    try:
        carrito = session.get('carrito', [])
        if not carrito:
            return jsonify({'exito': False, 'error': 'El carrito está vacío'}), 400
        
        usuario_id = session.get('usuario_id')
        if not usuario_id:
            return jsonify({'exito': False, 'error': 'Usuario no autenticado'}), 401
        
        total = sum(item['subtotal'] for item in carrito)
        items = []
        
        for item in carrito:
            # Manejar tanto cantidad directa como unidades por peso/paquete
            unidades = item.get('unidades', item['cantidad'])
            items.append({
                'producto_id': item['producto_id'],
                'cantidad': unidades,
                'precio_unitario': item['precio'] / unidades if 'unidades' in item else item['precio']
            })
        
        resultado = controller_resumen.procesar_venta(total, usuario_id, items)
        
        if resultado:
            # Actualizar stock de productos
            for item in carrito:
                producto = Producto.query.get(item['producto_id'])
                if producto:
                    unidades_vendidas = item.get('unidades', item['cantidad'])
                    producto.cantidad -= unidades_vendidas
                    db.session.commit()
            
            nombre_archivo = controller_resumen.generar_ticket(resultado)
            
            session['carrito'] = []
            session.modified = True
            
            return jsonify({
                'exito': True,
                'mensaje': 'Venta procesada con éxito',
                'url_ticket': url_for('venta.descargar_ticket', venta_id=resultado.id)
            })
        else:
            return jsonify({'exito': False, 'error': 'Error al procesar la venta'}), 500
            
    except Exception as e:
        print(f"Error en procesar_venta: {str(e)}")
        return jsonify({
            'exito': False,
            'error': 'Error interno del servidor'
        }), 500

@venta_bp.route('/api/corte_ventas', methods=['GET'])
def corte_ventas():
    try:
        reporte = controller_resumen.generar_reporte_diario()
        nombre_archivo = controller_resumen.generar_reporte_pdf(reporte)
        
        return jsonify({
            'exito': True,
            'reporte': reporte,
            'url_pdf': f'/descargar_reporte/{datetime.now().strftime("%Y%m%d")}'
        })
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': str(e)
        }), 500

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
    try:
        productos = controller_ventas.obtener_productos()
        productos_data = []
        
        for producto in productos:
            productos_data.append({
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': producto.precio,
                'imagen': producto.imagen if producto.imagen else None,
                'descripcion': producto.descripcion,
                'cantidad': producto.cantidad,
                'activo': producto.activo
            })
        
        return jsonify(productos_data)
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': str(e)
        }), 500