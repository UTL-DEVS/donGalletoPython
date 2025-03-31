from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash, send_file, send_from_directory
from datetime import datetime
from models import Galleta, resumen
from models.usuario import Usuario
from forms.form_galleta import GalletaForm
from controller import controller_galleta
from controller import controller_resumen
from utils.db import db
from cqrs import cqrs_galleta, cqrs_resumen
from flask_wtf.csrf import validate_csrf
import traceback
import os

galleta_bp = Blueprint('venta', __name__, template_folder='templates')

TICKETS_FOLDER = 'tickets'
if not os.path.exists(TICKETS_FOLDER):
    os.makedirs(TICKETS_FOLDER)

@galleta_bp.route('/tickets/<int:venta_id>')
def descargar_ticket(venta_id):
    try:
        filename = f'ticket_{venta_id}.pdf'
        filepath = os.path.join(TICKETS_FOLDER, filename)
        
        if not os.path.exists(filepath):
            from controller import controller_resumen
            venta = resumen.query.get_or_404(venta_id)
            controller_resumen.generar_ticket(venta)
            
        return send_from_directory(
            TICKETS_FOLDER,
            filename,
            as_attachment=True,
            mimetype='application/pdf'
        )
    except Exception as e:
        print(f"Error al descargar ticket: {str(e)}")
        return "Error al generar el ticket", 500
    
@galleta_bp.route('/tipo_venta')
def tipo_venta():
    return render_template('pages/pages-ventas/tipo_venta.html')

@galleta_bp.before_request
def antes_de_peticion():
    if 'carrito' not in session:
        session['carrito'] = []

@galleta_bp.route('/api/procesar_venta', methods=['POST'])
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

        item_required_fields = {
            'unidad': ['galleta_id', 'cantidad', 'precio_unitario', 'subtotal'],
            'peso': ['galleta_id', 'unidades', 'precio_unitario', 'subtotal', 'tipo_venta'],
            'paquete': ['galleta_id', 'unidades', 'precio_unitario', 'subtotal', 'tipo_venta']
        }

        for i, item in enumerate(items):
            tipo = item.get('tipo_venta', 'unidad')
            required = item_required_fields.get(tipo, item_required_fields['unidad'])
            
            if not all(field in item for field in required):
                return jsonify({
                    'exito': False,
                    'error': f'Item {i} incompleto para tipo {tipo}. Campos requeridos: {required}'
                }), 400

        venta = controller_resumen.procesar_venta(total, items)
        
        if not venta:
            return jsonify({
                'exito': False,
                'error': 'No se pudo crear la venta en la base de datos'
            }), 500

        try:
            ticket_path = controller_resumen.generar_ticket(venta)
            
            if not os.path.exists(ticket_path):
                raise FileNotFoundError("El archivo del ticket no se creó correctamente")
                
            return jsonify({
                'exito': True,
                'mensaje': 'Venta completada exitosamente',
                'venta_id': venta.id,
                'url_ticket': f'/tickets/{venta.id}'
            })
            
        except Exception as e:
            print(f"Error generando ticket: {str(e)}")
            return jsonify({
                'exito': True,
                'mensaje': 'Venta completada (pero no se generó el ticket)',
                'venta_id': venta.id,
                'error_ticket': str(e)
            })

    except Exception as e:
        print(f"Error en procesar_venta: {str(e)}")
        return jsonify({
            'exito': False,
            'error': str(e),
            'detalle': 'Error al procesar la venta'
        }), 500
    
@galleta_bp.route('/ventas')
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

@galleta_bp.route('/api/agregar_carrito', methods=['POST'])
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

@galleta_bp.route('/api/eliminar_del_carrito/<int:galleta_id>', methods=['DELETE'])
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

@galleta_bp.route('/api/vaciar_carrito', methods=['POST'])
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


@galleta_bp.route('/agregar_galleta', methods=['GET', 'POST'])
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
        
        galleta = controller_galleta.agregar_galleta(galleta_data, imagen_file)
        
        if galleta:
            flash('Galleta agregada correctamente', 'success')
            return redirect(url_for('receta.receta_index'))
        else:
            flash('Error: Verifica los datos de la galleta (nombre, precio, cantidad e imagen válida)', 'danger')
    
    return render_template('pages/pages-ventas/agregar_galleta.html', form=form)

@galleta_bp.route('/api/galletas')
def api_galletas():
    try:
        galletas = controller_galleta.obtener_galletas()
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
    
@galleta_bp.route('/listar_ventas')
def listar_ventas():
    from models.resumen import Venta
    
    ventas = Venta.query.order_by(Venta.fecha.desc()).all()
    return render_template('pages/pages-ventas/cancelar_venta.html', lista_ventas=ventas)

@galleta_bp.route('/eliminar_venta/<int:venta_id>', methods=['POST'])
def eliminar_venta(venta_id):
    try:
        from models.resumen import Venta
        from models import DetalleVenta 
        
        DetalleVenta.query.filter_by(venta_id=venta_id).delete()
        
        venta = Venta.query.get_or_404(venta_id)
        db.session.delete(venta)
        
        ticket_path = os.path.join(TICKETS_FOLDER, f'ticket_{venta_id}.pdf')
        if os.path.exists(ticket_path):
            os.remove(ticket_path)
            
        db.session.commit()
        flash('Venta cancelada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cancelar venta: {str(e)}', 'danger')
        app.logger.error(f"Error eliminando venta {venta_id}: {str(e)}")
    
    return redirect(url_for('venta.listar_ventas'))

@galleta_bp.route('/api/venta/<int:venta_id>')
def get_venta(venta_id):
    try:
        from models.resumen import Venta, DetalleVenta
        from models import Galleta  
        
        venta = Venta.query.get_or_404(venta_id)
        
        return jsonify({
            'id': venta.id,
            'total': venta.total,
            'fecha': venta.fecha.isoformat(),
            'estado': venta.estado,
            'detalles': [{
                'galleta_nombre': detalle.galleta.nombre_galleta if detalle.galleta else 'No disponible',
                'cantidad': detalle.cantidad,
                'precio_unitario': detalle.precio_unitario,
                'subtotal': detalle.subtotal,
                'tipo_venta': detalle.tipo_venta
            } for detalle in venta.detalles]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500