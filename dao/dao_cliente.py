from models.galleta import Galleta
from models.pedido import Pedido, DetallePedido
from utils.db import db
from datetime import datetime

class dao_cliente:
    @staticmethod
    def obtener_galletas_activas():
        return db.session.query(
        Galleta.id_galleta,
        Galleta.nombre_galleta,
        Galleta.precio_galleta,
        Galleta.imagen_galleta,
        Galleta.descripcion_galleta,
        # Opción 1: Si la columna existe como cantidad_galleta en la BD
        Galleta.cantidad_galleta,
        # Opción 2: Si necesitas un valor fijo (0) porque la columna no existe
        # db.literal(0).label('cantidad_galleta'),
        Galleta.fecha_creacion,
        Galleta.activo
    ).filter(Galleta.activo == True).all()
    
    @staticmethod
    def obtener_galleta_por_id(id_galleta):
        return db.session.query(
        Galleta.id_galleta,
        Galleta.nombre_galleta,
        Galleta.precio_galleta,
        Galleta.imagen_galleta,
        Galleta.descripcion_galleta,
        Galleta.cantidad_galleta,
        Galleta.fecha_creacion,
        Galleta.activo
    ).filter_by(id_galleta=id_galleta).first()
    
    @staticmethod
    def crear_pedido(id_usuario, carrito):
        try:
            total = sum(item['precio'] * item['cantidad'] for item in carrito)
            
            nuevo_pedido = Pedido(
                id_usuario=id_usuario,
                total=total,
                estatus='en proceso',
            )
            db.session.add(nuevo_pedido)
            db.session.flush()
            
            for item in carrito:
                detalle = DetallePedido(
                    id_pedido=nuevo_pedido.id_pedido,
                    id_galleta=item['id'],
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio'],
                    tipo_pedido=item['tipo_pedido']
                )
                db.session.add(detalle)
            
            db.session.commit()
            return nuevo_pedido
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def obtener_pedido_por_id(id_pedido):
        return Pedido.query.get(id_pedido)
    
    @staticmethod
    def obtenerPedidos():
        return Pedido.query.all()
        return Pedido.query.get(id_pedido)
