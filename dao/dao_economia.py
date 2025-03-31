from utils import db, func
from models import Venta
from datetime import datetime, timedelta

def obtener_ventas_por_mes(mes, dias):
        # Convertir el mes en un rango de fechas
        mes_numero,anio = map(str, str(mes).split('/'))
        ultimo_dia = datetime(int(anio), int(mes_numero), 1).replace(day=28) + timedelta(days=4)
        ultimo_dia = ultimo_dia - timedelta(days=ultimo_dia.day)  # Último día del mes
        primer_dia = ultimo_dia - timedelta(days=int(dias) - 1)

        return (
            db.session.query(Venta)
            .filter(Venta.fecha.between(primer_dia, ultimo_dia))
            #.filter(Venta.estatus != 0)  # Solo Ventas activas
            .all()
        )

def obtener_primera_fecha_venta():
    primera_fecha_venta = (db.session.query(func.date_format(Venta.fecha,  "%m/%Y"))
            .order_by(Venta.fecha.asc())
            .limit(1)
            .scalar())
    return primera_fecha_venta
        
def obtener_ultima_fecha_venta():
    ultima_fecha_venta = (db.session.query(func.date_format(Venta.fecha,  "%m/%Y"))
        .order_by(Venta.fecha.desc())
        .limit(1)
        .scalar()
        )
    return ultima_fecha_venta