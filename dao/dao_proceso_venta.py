from models import Galleta, Stock
from models.ProcesoVenta import ProcesoVenta
from utils import db

class ProcesoVentaDAO:
    @staticmethod
    def obtener_galletas_activas():
        return Galleta.query.filter_by(activo=True).all()
    
    @staticmethod
    def obtener_galleta_por_id(galleta_id):
        return Galleta.query.get(galleta_id)
    
    @staticmethod
    def obtener_ventas():
        return ProcesoVenta.query.order_by(ProcesoVenta.fecha.desc()).all()
    
    @staticmethod
    def obtener_venta_por_id(venta_id):
        return ProcesoVenta.query.get(venta_id)
    
    @staticmethod
    def eliminar_venta(venta_id):
        venta = ProcesoVenta.query.get(venta_id)
        if venta:
            for detalle in venta.detalles:
                stock = Stock.query.filter_by(id_galleta=detalle.galleta_id).first()
                if stock:
                    stock.cantidad_galleta += detalle.cantidad
            
            db.session.delete(venta)
            db.session.commit()
            return True
        return False