from models.pedido import Pedido
from models import Galleta
from utils.db import db

class PedidoController:
    @staticmethod
    def obtener_pedidos_completados(id_usuario=None):
        try:
            query = Pedido.query.filter_by(estatus='completado').order_by(Pedido.fecha_pedido.desc())
            if id_usuario:
                query = query.filter_by(id_usuario=id_usuario)
            pedidos = query.all()
            
            return pedidos
        except Exception as e:
            print(f"Error al obtener pedidos completados: {str(e)}")
            return []

    @staticmethod
    def cargar_pedido_a_carrito(session, id_pedido):
        pedido = Pedido.query.get(id_pedido)
        if not pedido or pedido.estatus != 'completado':
            raise ValueError("Pedido no encontrado o no está completado")
        
        carrito = session.get('carrito', [])
        
        for detalle in pedido.detalles:
            item_existente = next(
                (item for item in carrito 
                 if item['galleta_id'] == detalle.id_galleta and item['tipo_venta'] == detalle.tipo_pedido),
                None
            )
            
            if item_existente:
                if detalle.tipo_pedido == 'unidad':
                    item_existente['cantidad'] += detalle.cantidad
                    item_existente['unidades_equivalentes'] += detalle.cantidad
                elif detalle.tipo_pedido == 'peso':
                    item_existente['gramos'] += detalle.cantidad
                    item_existente['unidades_equivalentes'] += detalle.cantidad / 10
                elif detalle.tipo_pedido == 'paquete':
                    item_existente['cantidad_paquetes'] += 1
                    item_existente['unidades_equivalentes'] += detalle.cantidad
            else:
                galleta = Galleta.query.get(detalle.id_galleta)
                if not galleta:
                    continue
                
                nuevo_item = {
                    'galleta_id': detalle.id_galleta,
                    'nombre': galleta.nombre_galleta,
                    'precio_unitario': detalle.precio_unitario,
                    'tipo_venta': detalle.tipo_pedido,
                    'subtotal': detalle.cantidad * detalle.precio_unitario,
                    'unidades_equivalentes': detalle.cantidad,
                    'metadata_json': {}
                }
                
                if detalle.tipo_pedido == 'unidad':
                    nuevo_item['cantidad'] = detalle.cantidad
                elif detalle.tipo_pedido == 'peso':
                    nuevo_item['gramos'] = detalle.cantidad
                elif detalle.tipo_pedido == 'paquete':
                    nuevo_item['cantidad_paquetes'] = 1
                
                carrito.append(nuevo_item)
        
        session['carrito'] = carrito
        session.modified = True
        return carrito