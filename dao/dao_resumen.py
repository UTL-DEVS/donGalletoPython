from models import Venta, DetalleVenta, Galleta
from utils.db import db
from datetime import datetime

def crear_venta(total, usuario_id, items):
    try:
        nueva_venta = Venta(
            total=total,
            usuario_id=usuario_id,
            fecha=datetime.utcnow(),
            estado='completada'
        )
        
        db.session.add(nueva_venta)
        
        for item in items:
            galleta = Galleta.query.get(item['galleta_id'])
            if galleta:
                detalle = DetalleVenta(
                    venta=nueva_venta,
                    galleta_id=item['galleta_id'],
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio_unitario'],
                    subtotal=item['subtotal']
                )
                db.session.add(detalle)
        
        db.session.commit()
        return nueva_venta
    except Exception as e:
        print(f"Error al crear venta: {str(e)}")
        db.session.rollback()
        return None

def obtener_ventas_del_dia():
    hoy = datetime.now().date()
    return Venta.query.filter(
        db.func.date(Venta.fecha) == hoy,
        Venta.estado == 'completada'
    ).all()

def generar_reporte_ventas(ventas):
    reporte = {
        'total_ventas': len(ventas),
        'total_ingresos': sum(v.total for v in ventas),
        'detalle': []
    }
    
    for venta in ventas:
        reporte['detalle'].append({
            'id': venta.id,
            'fecha': venta.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'total': venta.total,
            'items': [{
                'galleta': detalle.galleta.nombre_galleta,
                'cantidad': detalle.cantidad,
                'precio_unitario': detalle.precio_unitario,
                'subtotal': detalle.subtotal
            } for detalle in venta.detalles]
        })
    
    return reporte