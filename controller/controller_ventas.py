from dao import dao_ventas
from cqrs import cqrs_ventas
from models import Producto
from fpdf import FPDF
from datetime import datetime

def agregar_producto(form_data, imagen_file):
    if not cqrs_ventas.validar_producto(form_data):
        return None
    
    return dao_ventas.crear_producto(
        nombre=form_data['nombre'],
        precio=form_data['precio'],
        descripcion=form_data.get('descripcion', ''),
        imagen_file=imagen_file,
        cantidad=form_data.get('cantidad', 0)
    )

def obtener_productos():
    return dao_ventas.obtener_productos_activos()

def obtener_producto(producto_id):
    return dao_ventas.obtener_producto_por_id(producto_id)

def generar_reporte_pdf(reporte):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Don Galleto - Corte de Ventas", ln=1, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Fecha del reporte: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
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
        pdf.cell(200, 10, txt=f"Venta #{venta['id']} - {venta['fecha']} - Total: ${venta['total']:.2f}", ln=1)
        pdf.set_font("Arial", size=10)
        
        pdf.cell(100, 10, txt="Producto", border=1)
        pdf.cell(30, 10, txt="Cantidad", border=1)
        pdf.cell(30, 10, txt="Precio Unit.", border=1)
        pdf.cell(30, 10, txt="Subtotal", border=1, ln=1)
        
        for item in venta['items']:
            pdf.cell(100, 10, txt=item['producto'], border=1)
            pdf.cell(30, 10, txt=str(item['cantidad']), border=1)
            pdf.cell(30, 10, txt=f"${item['precio_unitario']:.2f}", border=1)
            pdf.cell(30, 10, txt=f"${item['subtotal']:.2f}", border=1, ln=1)
        
        pdf.ln(5)
    
    nombre_archivo = f"corte_ventas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(nombre_archivo)
    return nombre_archivo