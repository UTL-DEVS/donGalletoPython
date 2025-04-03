from models import ResumenVenta

class ResumenVentaDAO:
    @staticmethod
    def obtener_cortes():
        return ResumenVenta.query.order_by(ResumenVenta.fecha_corte.desc()).all()
    
    @staticmethod
    def obtener_corte_por_fecha(fecha):
        return ResumenVenta.query.filter_by(fecha_corte=fecha).first()