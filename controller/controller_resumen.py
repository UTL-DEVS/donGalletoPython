from dao import dao_resumen, dao_ventas
from cqrs import cqrs_resumen
from datetime import datetime
from models.resumen import Venta, DetalleVenta
from fpdf import FPDF
from utils.db import db

def procesar_venta(total, items):
    try:
        from models.resumen import Venta, DetalleVenta 
        
        if not items or total <= 0:
            raise ValueError("Carrito vacío o total inválido")

        nueva_venta = Venta(
            total=total,
            fecha=datetime.now(),
            estado='completada'
        )
        db.session.add(nueva_venta)
        db.session.flush()

        for item in items:
            detalle = DetalleVenta(
                venta_id=nueva_venta.id,
                galleta_id=item['galleta_id'],
                cantidad=item['cantidad'],
                precio_unitario=item['precio_unitario'],
                subtotal=item['subtotal'],
                tipo_venta=item.get('tipo_venta', 'unidad')
            )
            db.session.add(detalle)

        db.session.commit()
        return nueva_venta

    except Exception as e:
        db.session.rollback()
        print(f"Error al procesar venta: {str(e)}")
        print(traceback.format_exc()) 
        raise 
    
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
    
    pdf.cell(100, 10, txt="Galleta", border=1)
    pdf.cell(30, 10, txt="Cantidad", border=1)
    pdf.cell(30, 10, txt="Precio", border=1)
    pdf.cell(30, 10, txt="Subtotal", border=1, ln=1)
    
    for detalle in venta.detalles:
        pdf.cell(100, 10, txt=detalle.galleta.nombre_galleta, border=1)
        pdf.cell(30, 10, txt=str(detalle.cantidad), border=1)
        pdf.cell(30, 10, txt=f"${detalle.precio_unitario:.2f}", border=1)
        pdf.cell(30, 10, txt=f"${detalle.subtotal:.2f}", border=1, ln=1)
    
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Total: ${venta.total:.2f}", ln=1, align="R")
    
    nombre_archivo = f"ticket_{venta.id}.pdf"
    pdf.output(nombre_archivo)
    return nombre_archivo