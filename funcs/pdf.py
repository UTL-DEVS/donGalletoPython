import pdfkit
from models.ProcesoVenta import ProcesoVenta

def generar_pdf_venta(venta_id):
    venta = ProcesoVenta.query.get(venta_id)
    if not venta:
        return False
    
    html = f"""
    <h1>Comprobante de Venta #{venta.id}</h1>
    <p>Fecha: {venta.fecha.strftime('%d/%m/%Y %H:%M')}</p>
    <h3>Detalles:</h3>
    <ul>
    {"".join(f"<li>{d.galleta.nombre_galleta} - {d.cantidad} x ${d.precio_unitario} = ${d.subtotal}</li>" for d in venta.detalles)}
    </ul>
    <h2>Total: ${venta.total}</h2>
    """
    
    try:
        options = {
            'encoding': 'UTF-8',
            'quiet': ''
        }
        pdfkit.from_string(html, f'comprobantes/venta_{venta.id}.pdf', options=options)
        return True
    except Exception as e:
        print(f"Error generando PDF: {str(e)}")
        return False