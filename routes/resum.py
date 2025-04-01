from flask import Blueprint, render_template, request, jsonify, session, send_file
import os
from models import Usuario
from datetime import datetime
from controller import controller_resumen

resumen_bp = Blueprint('resumen', __name__, template_folder='templates')

CORTE_FOLDER = 'cortes'
if not os.path.exists(CORTE_FOLDER):
    os.makedirs(CORTE_FOLDER)

@resumen_bp.route('/resumen')
def resumen():
    return render_template('pages/page-resumen/resumen.html')

@resumen_bp.route('/api/agregar_carrito', methods=['POST'])
def agregar_carrito():
    data = request.get_json()
    if not data or 'items' not in data:
        return jsonify({'success': False, 'error': 'Datos inválidos'})
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'success': False, 'error': 'Token no proporcionado'}), 401
    
    token = auth_header.split(' ')[1]
    
    usuario = Usuario.validar_token(token)
    if not usuario:
        return jsonify({'success': False, 'error': 'Token inválido'}), 401
    
    venta = controller_resumen.procesar_venta(
        total=data['total'],
        usuario_id=usuario.id,
        items=data['items']
    )
    
    if venta:
        ticket_path = controller_resumen.generar_ticket(venta)
        return jsonify({
            'success': True,
            'ticket_url': f'/descargar_ticket/{venta.id}'
        })
    else:
        return jsonify({'success': False, 'error': 'Error al procesar la venta'})


@resumen_bp.route('/descargar_ticket/<int:venta_id>')
def descargar_ticket(venta_id):
    ticket_path = f"ticket_{venta_id}.pdf"
    if os.path.exists(ticket_path):
        return send_file(ticket_path, as_attachment=True)
    return "Ticket no encontrado", 404

@resumen_bp.route('/api/corte_ventas', methods=['GET'])
def api_corte_ventas():
    try:
        filepath, error = controller_resumen.corte_ventas()
        
        if error:
            return jsonify({'success': False, 'error': error}), 400
            
        filename = os.path.basename(filepath)
        return jsonify({
            'success': True,
            'url': f'/descargar_corte/{filename}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@resumen_bp.route('/descargar_corte/<filename>')
def descargar_corte(filename):
    filepath = os.path.join(controller_resumen.CORTE_FOLDER, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, mimetype='application/pdf')
    return "Archivo no encontrado", 404