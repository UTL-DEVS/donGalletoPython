from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash, send_file
from datetime import datetime
from models import Galleta, usuario
from models.usuario import Usuario
from forms.form_ventas import GalletaForm
from controller import controller_ventas
from controller import controller_resumen
from utils.db import db
from cqrs import cqrs_resumen, cqrs_ventas
from flask_wtf.csrf import validate_csrf
import traceback

venta_bp = Blueprint('venta', __name__, template_folder='templates')

@venta_bp.route('/tipo_venta')
def tipo_venta():
    return render_template('pages/pages-ventas/tipo_venta.html')

@venta_bp.before_request
def antes_de_peticion():
    if 'carrito' not in session:
        session['carrito'] = []

@venta_bp.route('/api/procesar_venta', methods=['POST'])
def procesar_venta():
    try:
        validate_csrf(request.headers.get('X-CSRFToken'))
        
        if not request.is_json:
            return jsonify({
                'exito': False,
                'error': 'Se esperaba formato JSON'
            }), 400

        data = request.get_json()
        
        required_fields = ['items', 'total']
        if not all(field in data for field in required_fields):
            return jsonify({
                'exito': False,
                'error': f'Faltan campos requeridos: {required_fields}'
            }), 400

        items = data['items']
        total = float(data['total'])

        item_required_fields = ['galleta_id', 'cantidad', 'precio_unitario', 'subtotal']
        for i, item in enumerate(items):
            if not all(field in item for field in item_required_fields):
                return jsonify({
                    'exito': False,
                    'error': f'Item {i} incompleto. Campos requeridos: {item_required_fields}'
                }), 400

        venta = controller_resumen.procesar_venta(total, items)
        
        if not venta:
            return jsonify({
                'exito': False,
                'error': 'No se pudo crear la venta en la base de datos'
            }), 500

        return jsonify({
            'exito': True,
            'mensaje': 'Venta procesada exitosamente',
            'venta_id': venta.id,
            'url_ticket': f'/tickets/{venta.id}'
        })

    except Exception as e:
        print(f"Error en ruta /api/procesar_venta: {str(e)}")
        print(traceback.format_exc())
        
        return jsonify({
            'exito': False,
            'error': 'Error interno del servidor al procesar la venta',
            'detalle': str(e)
        }), 500
    
@venta_bp.route('/ventas')
def ventas():
    tipo_venta = request.args.get('tipo', 'unidad')
    galletas = Galleta.query.filter_by(activo=True).all()
    
    carrito = session.get('carrito', [])
    total = sum(item['subtotal'] for item in carrito)
    
    return render_template('pages/pages-ventas/ventas.html', 
                         galletas=galletas, 
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
        
        campos_requeridos = ['galleta_id', 'cantidad', 'galleta_nombre', 'precio', 'tipo_venta']
        for campo in campos_requeridos:
            if campo not in datos:
                return jsonify({
                    'exito': False,
                    'error': f'Falta el campo requerido: {campo}'
                }), 400

        try:
            galleta_id = int(datos['galleta_id'])
            cantidad = int(datos['cantidad'])
            precio = float(datos['precio'])
            unidades = int(datos.get('unidades', cantidad))
            galleta_nombre = str(datos['galleta_nombre'])
            tipo_venta = str(datos['tipo_venta'])
        except (ValueError, TypeError) as e:
            return jsonify({
                'exito': False,
                'error': 'Tipos de datos inválidos'
            }), 400

        carrito = session.get('carrito', [])
        
        item_existente = next(
            (item for item in carrito 
             if (item['galleta_id'] == galleta_id and 
                 item['nombre'] == galleta_nombre and
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
                'galleta_id': galleta_id,
                'nombre': galleta_nombre,
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
            'mensaje': 'Galleta agregada al carrito'
        })
        
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': str(e)
        }), 500

@venta_bp.route('/api/eliminar_del_carrito/<int:galleta_id>', methods=['DELETE'])
def eliminar_del_carrito(galleta_id):
    try:
        data = request.get_json()
        galleta_nombre = data.get('galleta_nombre')
        tipo_venta = data.get('tipo_venta')
        
        if not galleta_nombre or not tipo_venta:
            return jsonify({
                'exito': False,
                'error': 'Faltan datos para identificar la galleta'
            }), 400
        
        carrito = session.get('carrito', [])
        nuevo_carrito = [
            item for item in carrito 
            if not (item['galleta_id'] == galleta_id and 
                   item['nombre'] == galleta_nombre and
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

@venta_bp.route('/agregar_galleta', methods=['GET', 'POST'])
def agregar_galleta():
    form = GalletaForm()
    
    if form.validate_on_submit():
        imagen_file = request.files.get('imagen_galleta')
        
        galleta_data = {
            'nombre_galleta': form.nombre_galleta.data.strip(),
            'precio_galleta': form.precio_galleta.data,
            'descripcion_galleta': form.descripcion_galleta.data.strip(),
            'cantidad_galleta': form.cantidad_galleta.data
        }
        
        galleta = controller_ventas.agregar_galleta(galleta_data, imagen_file)
        
        if galleta:
            flash('Galleta agregada correctamente', 'success')
            return redirect(url_for('venta.ventas'))
        else:
            flash('Error: Verifica los datos de la galleta (nombre, precio, cantidad e imagen válida)', 'danger')
    
    return render_template('pages/pages-ventas/agregar_galleta.html', form=form)

@venta_bp.route('/api/galletas')
def api_galletas():
    try:
        galletas = controller_ventas.obtener_galletas()
        galletas_data = []
        
        for galleta in galletas:
            galletas_data.append({
                'id': galleta.id_galleta,
                'nombre': galleta.nombre_galleta,
                'precio': galleta.precio_galleta,
                'imagen': galleta.imagen_galleta if galleta.imagen_galleta else None,
                'descripcion': galleta.descripcion_galleta,
                'cantidad': galleta.cantidad_galleta,
                'activo': galleta.activo
            })
        
        return jsonify(galletas_data)
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': str(e)
        }), 500