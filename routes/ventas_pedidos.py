from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import IntegerField, HiddenField
from models.pedido import Pedido, DetallePedido
from models.galleta import Galleta
from utils.db import db
from datetime import datetime

pedidos_ventas_bp = Blueprint('pedidos_ventas', __name__, template_folder='templates')

USUARIO_DEFAULT = 4 

class PedidoVentaForm(FlaskForm):
    id_galleta = HiddenField()
    cantidad = IntegerField('Cantidad', default=1)
    tipo_pedido = HiddenField(default='unidad')

@pedidos_ventas_bp.route('/ventas/pedidos')
def inicio():
    return redirect(url_for('pedidos_ventas.nuevo_pedido'))

@pedidos_ventas_bp.route('/ventas/pedidos/nuevo', methods=['GET'])
def nuevo_pedido():
    form = PedidoVentaForm()
    galletas = Galleta.query.filter_by(activo=True).order_by(Galleta.nombre_galleta).all()
    
    return render_template('pages/pages-ventas/crear_pedido.html',
                        form=form,
                        galletas=galletas)

@pedidos_ventas_bp.route('/ventas/pedidos/crear', methods=['POST'])
def crear_pedido():
    try:
        id_galletas = request.form.getlist('id_galleta[]')
        cantidades = request.form.getlist('cantidad[]')
        
        if not id_galletas:
            return jsonify({'error': 'No se seleccionaron productos'}), 400

        # Crear pedido
        nuevo_pedido = Pedido(
            id_usuario=USUARIO_VENTAS_DIRECTAS,
            total=0,
            fecha_pedido=datetime.now(),
            estatus='completado',
            observaciones='Venta directa individual'
        )
        db.session.add(nuevo_pedido)
        db.session.flush()

        # Procesar productos
        total = 0
        for i, id_galleta in enumerate(id_galletas):
            galleta = Galleta.query.get(id_galleta)
            if galleta and galleta.activo:
                cantidad = int(cantidades[i]) if cantidades[i] else 0
                if cantidad > 0:
                    subtotal = float(galleta.precio_galleta) * cantidad
                    total += subtotal

                    DetallePedido(
                        id_pedido=nuevo_pedido.id_pedido,
                        id_galleta=id_galleta,
                        cantidad=cantidad,
                        precio_unitario=galleta.precio_galleta,
                        tipo_pedido='unidad'
                    ).save()

        # Actualizar total
        nuevo_pedido.total = total
        db.session.commit()

        return jsonify({
            'success': True,
            'pedido_id': nuevo_pedido.id_pedido,
            'total': total
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500