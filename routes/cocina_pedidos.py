from flask import Blueprint, render_template
from dao import dao_produccion
from routes.cliente import cliente_bp
from models.pedido import Pedido, DetallePedido
from models.galleta import Galleta
from models.usuario import Usuario
from models.persona import Persona
from utils.db import db

cocina_pedidos_bp = Blueprint('cocina-pedidos', __name__, template_folder='templates')

@cocina_pedidos_bp.route('/cocina-pedidos')
def cocina_pedidos():
    pedidos = dao_produccion.obtenerPedidos()
    print('usuario: ',pedidos)
    
    return render_template('pages/page-produccion/cocina-pedidos/pedidos.html', lstPedidos = pedidos)


# (Pedido.query, Usuario.query
#         .order_by(Pedido.fecha_pedido.desc())
#         .options(db.joinedload(Pedido.detalles))
#         .all())

# resultados = db.session.query(
#         Produccion.fecha_produccion,
#         Produccion.hora_produccion,
#         Galleta.nombre_galleta,
#         DetalleProduccion.cantidad
#     ).select_from(Produccion)\
#     .join(DetalleProduccion)\
#     .join(Galleta)\
#     .filter(Produccion.fecha_produccion == fecha)\
#     .all()