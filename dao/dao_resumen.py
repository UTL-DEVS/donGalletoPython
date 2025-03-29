from models import Venta, DetalleVenta, Producto
from utils.db import db
from datetime import datetime

def crear_venta(total, usuario_id, items):
    nueva_venta = Venta(
        total=total,
        usuario_id=usuario_id
    )
    
    db.session.add(nueva_venta)
    
    for item in items:
        producto = Producto.query.get(item['producto_id'])
        if producto:
            detalle = DetalleVenta(
                venta=nueva_venta,
                producto_id=item['producto_id'],
                cantidad=item['cantidad'],
                precio_unitario=producto.precio,
                subtotal=producto.precio * item['cantidad']
            )
            db.session.add(detalle)
    
    db.session.commit()
    return nueva_venta

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
                'producto': detalle.producto.nombre,
                'cantidad': detalle.cantidad,
                'precio_unitario': detalle.precio_unitario,
                'subtotal': detalle.subtotal
            } for detalle in venta.detalles]
        })
    
    return reporte