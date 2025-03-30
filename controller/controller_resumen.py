from dao import dao_resumen, dao_ventas
from cqrs import cqrs_resumen
from datetime import datetime
from fpdf import FPDF

def procesar_venta(total, usuario_id, items):
    for item in items:
        if not cqrs_resumen.validar_item_carrito(item):
            return None
    
    for item in items:
        producto = dao_ventas.obtener_producto_por_id(item['producto_id'])
        if not producto or producto.cantidad < item['cantidad']:
            return None
    
    venta = dao_resumen.crear_venta(total, usuario_id, items)
    
    if venta:
        for item in items:
            producto = dao_ventas.obtener_producto_por_id(item['producto_id'])
            if producto:
                producto.cantidad -= item['cantidad']
                db.session.commit()
    
    return venta

def generar_reporte_diario():
    ventas = dao_resumen.obtener_ventas_del_dia()
    return dao_resumen.generar_reporte_ventas(ventas)

def generar_ticket(venta):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Don Galleto", ln=1, align="C")
    pdf.cell(200, 10, txt="Ticket de Venta", ln=1, align="C")
    pdf.cell(200, 10, txt=f"Fecha: {venta.fecha.strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
    pdf.cell(200, 10, txt=f"Venta ID: {venta.id}", ln=1)
    pdf.ln(5)
    
    pdf.cell(100, 10, txt="Producto", border=1)
    pdf.cell(30, 10, txt="Cantidad", border=1)
    pdf.cell(30, 10, txt="Precio", border=1)
    pdf.cell(30, 10, txt="Subtotal", border=1, ln=1)
    
    for detalle in venta.detalles:
        pdf.cell(100, 10, txt=detalle.producto.nombre, border=1)
        pdf.cell(30, 10, txt=str(detalle.cantidad), border=1)
        pdf.cell(30, 10, txt=f"${detalle.precio_unitario:.2f}", border=1)
        pdf.cell(30, 10, txt=f"${detalle.subtotal:.2f}", border=1, ln=1)
    
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Total: ${venta.total:.2f}", ln=1, align="R")
    
    nombre_archivo = f"ticket_{venta.id}.pdf"
    pdf.output(nombre_archivo)
    return nombre_archivo