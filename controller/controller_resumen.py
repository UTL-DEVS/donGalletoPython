from dao import dao_galleta, dao_resumen
from cqrs import cqrs_resumen
from datetime import datetime
from models import Venta, DetalleVenta, Galleta
from fpdf import FPDF
from utils.db import db
import os, traceback

TICKETS_FOLDER = 'tickets'
if not os.path.exists(TICKETS_FOLDER):
    os.makedirs(TICKETS_FOLDER)

CORTE_FOLDER = 'cortes'
if not os.path.exists(CORTE_FOLDER):
    os.makedirs(CORTE_FOLDER)

def procesar_venta(total, items):
    try:
        if not items or total <= 0:
            raise ValueError("Carrito vacío o total inválido")

        for item in items:
            galleta = Galleta.query.get(item['galleta_id'])
            if not galleta:
                raise ValueError(f"Galleta con ID {item['galleta_id']} no encontrada")
            
            if item.get('tipo_venta') == 'peso':
                cantidad_a_restar = item['unidades']
            elif item.get('tipo_venta') == 'paquete':
                cantidad_a_restar = item['unidades']
            else:  
                cantidad_a_restar = item['cantidad']
                
            if galleta.cantidad_galleta < cantidad_a_restar:
                raise ValueError(f"Stock insuficiente para {galleta.nombre_galleta}")

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

            galleta = Galleta.query.get(item['galleta_id'])
            if item.get('tipo_venta') == 'peso':
                galleta.cantidad_galleta -= item['unidades']
            elif item.get('tipo_venta') == 'paquete':
                galleta.cantidad_galleta -= item['unidades']
            else:
                galleta.cantidad_galleta -= item['cantidad']

        db.session.commit()
        return nueva_venta

    except Exception as e:
        db.session.rollback()
        print(f"Error al procesar venta: {str(e)}")
        raise
    
def generar_reporte_diario():
    ventas = dao_resumen.obtener_ventas_del_dia()
    return dao_resumen.generar_reporte_ventas(ventas)

def corte_ventas():
    try:
        hoy = datetime.now().date()
        ventas = Venta.query.filter(
            db.func.date(Venta.fecha) == hoy,
            Venta.estado == 'completada'
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
        filepath = os.path.join(CORTE_FOLDER, nombre_archivo)
        pdf.output(filepath)
        
        return filepath, None
        
    except Exception as e:
        print(f"Error al generar corte de ventas: {str(e)}")
        return None, str(e)
    
CORTE_FOLDER = 'cortes'
if not os.path.exists(CORTE_FOLDER):
    os.makedirs(CORTE_FOLDER)


def generar_ticket(venta):
    from fpdf import FPDF
    import os
    
    try:
        os.makedirs(TICKETS_FOLDER, exist_ok=True)
        
        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt="Don Galleto", ln=1, align="C")
        pdf.cell(200, 10, txt="Ticket de Venta", ln=1, align="C")
        
        pdf.cell(200, 10, txt=f"Fecha: {venta.fecha.strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
        pdf.cell(200, 10, txt=f"Venta ID: {venta.id}", ln=1)
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(100, 10, "Producto", border=1)
        pdf.cell(30, 10, "Cantidad", border=1)
        pdf.cell(30, 10, "P. Unit.", border=1)
        pdf.cell(30, 10, "Subtotal", border=1, ln=1)
        
        pdf.set_font("Arial", size=12)
        for detalle in venta.detalles:
            pdf.cell(100, 10, detalle.galleta.nombre_galleta, border=1)
            pdf.cell(30, 10, str(detalle.cantidad), border=1)
            pdf.cell(30, 10, f"${detalle.precio_unitario:.2f}", border=1)
            pdf.cell(30, 10, f"${detalle.subtotal:.2f}", border=1, ln=1)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(160, 10, "TOTAL:", border=0)
        pdf.cell(30, 10, f"${venta.total:.2f}", border=0, ln=1)
        
        filename = os.path.join(TICKETS_FOLDER, f"ticket_{venta.id}.pdf")
        pdf.output(filename)
        
        print(f"Ticket generado en: {filename}") 
        return filename
        
    except Exception as e:
        print(f"Error al generar ticket: {str(e)}")
        raise