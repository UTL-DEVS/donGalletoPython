from dao import dao_proceso_venta
from datetime import datetime
from models.ProcesoVenta import ProcesoVenta
from utils.db import db
import os
from fpdf import FPDF

TICKETS_FOLDER = 'tickets'
if not os.path.exists(TICKETS_FOLDER):
    os.makedirs(TICKETS_FOLDER)

CORTES_FOLDER = 'cortes'
if not os.path.exists(CORTES_FOLDER):
    os.makedirs(CORTES_FOLDER)

    
def generar_reporte_diario():
    ventas = dao_proceso_venta.obtener_ventas_del_dia()
    return dao_proceso_venta.generar_reporte_ventas(ventas)

def corte_ventas():
    from fpdf import FPDF
    import os
    try:
        hoy = datetime.now().date()
        ventas = ProcesoVenta.query.filter(
            db.func.date(ProcesoVenta.fecha) == hoy,
            ProcesoVenta.estado == 'completada'
        ).all()
        
        if not ventas:
            return None, "No hay ventas registradas hoy"
        
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
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Don Galleto - Corte de Ventas", ln=1, align="C")
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Fecha: {datetime.now().strftime('%Y-%m-%d')}", ln=1)
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Resumen General", ln=1)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Total de ventas: {reporte['total_ventas']}", ln=1)
        pdf.cell(200, 10, txt=f"Total de ingresos: ${reporte['total_ingresos']:.2f}", ln=1)
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Detalle de Ventas", ln=1)
        pdf.set_font("Arial", size=10)
        
        for venta in reporte['detalle']:
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt=f"Venta #{venta['id']} - {venta['fecha']}", ln=1)
            pdf.set_font("Arial", size=10)
            
            pdf.cell(80, 10, txt="Producto", border=1)
            pdf.cell(30, 10, txt="Cantidad", border=1)
            pdf.cell(30, 10, txt="P. Unit.", border=1)
            pdf.cell(30, 10, txt="Subtotal", border=1)
            pdf.cell(30, 10, txt="Hora", border=1, ln=1)
            
            for item in venta['items']:
                pdf.cell(80, 10, txt=item['galleta'], border=1)
                pdf.cell(30, 10, txt=str(item['cantidad']), border=1)
                pdf.cell(30, 10, txt=f"${item['precio_unitario']:.2f}", border=1)
                pdf.cell(30, 10, txt=f"${item['subtotal']:.2f}", border=1)
                pdf.cell(30, 10, txt=venta['fecha'].split(' ')[1][:8], border=1, ln=1)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(170, 10, txt="Total Venta:", border=0, align="R")
            pdf.cell(30, 10, txt=f"${venta['total']:.2f}", border=0, ln=1)
            pdf.ln(5)
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(170, 10, txt="TOTAL DEL DÍA:", border=0, align="R")
        pdf.cell(30, 10, txt=f"${reporte['total_ingresos']:.2f}", border=0, ln=1)
        
        nombre_archivo = f"corte_ventas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(CORTES_FOLDER, nombre_archivo)
        pdf.output(filepath)
        
        if not os.path.exists(filepath):
            raise Exception("No se pudo generar el archivo PDF")
            
        return filepath, None
        
    except Exception as e:
        print(f"Error al generar corte de ventas: {str(e)}")
        return None, str(e)