from flask import send_file
from models.Stock import Stock
from models.ProcesoVenta import ProcesoVenta, DetalleVenta
from utils.db import db
from fpdf import FPDF
import os, datetime

TICKETS_FOLDER = 'tickets'
os.makedirs(TICKETS_FOLDER, exist_ok=True)

class ProcesoVentaController:
    @staticmethod
    def agregar_al_carrito(session, galleta_id, nombre, precio, cantidad, tipo_venta):
        carrito = session.get('carrito', [])
        
        item = next((item for item in carrito 
                    if item['galleta_id'] == galleta_id 
                    and item['tipo_venta'] == tipo_venta), None)
        
        if item:
            if tipo_venta == 'unidad':
                item['cantidad'] += cantidad
            else:
                item['unidades'] += cantidad
            item['subtotal'] += precio * (cantidad if tipo_venta == 'unidad' else 1)
        else:
            carrito.append({
                'galleta_id': galleta_id,
                'nombre': nombre,
                'precio_unitario': precio,
                'subtotal': precio * (cantidad if tipo_venta == 'unidad' else 1),
                'tipo_venta': tipo_venta,
                'cantidad': cantidad if tipo_venta == 'unidad' else 1,
                'unidades': cantidad if tipo_venta != 'unidad' else 0
            })
        
        session['carrito'] = carrito
        return carrito

    @staticmethod
    def generar_ticket(venta):
        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Don Galleto - Ticket de Venta', 0, 1, 'C')
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'No. Venta: {venta.id}', 0, 1)
        pdf.cell(0, 10, f'Fecha: {venta.fecha.strftime("%d/%m/%Y %H:%M")}', 0, 1)
        pdf.ln(10)
        
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(100, 10, 'Producto', 1, 0)
        pdf.cell(30, 10, 'Cantidad', 1, 0)
        pdf.cell(30, 10, 'P. Unit.', 1, 0)
        pdf.cell(30, 10, 'Subtotal', 1, 1)
        
        pdf.set_font('Arial', '', 10)
        for detalle in venta.detalles:
            pdf.cell(100, 10, detalle.galleta.nombre_galleta, 1, 0)
            
            if detalle.tipo_venta == 'unidad':
                pdf.cell(30, 10, f"{detalle.cantidad} u", 1, 0)
            elif detalle.tipo_venta == 'peso':
                pdf.cell(30, 10, f"{detalle.cantidad * 10}g", 1, 0)
            else:
                pdf.cell(30, 10, f"Paq. {detalle.cantidad}u", 1, 0)
                
            pdf.cell(30, 10, f"${detalle.precio_unitario:.2f}", 1, 0)
            pdf.cell(30, 10, f"${detalle.subtotal:.2f}", 1, 1)
        
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f'TOTAL: ${venta.total:.2f}', 0, 1, 'R')
        
        os.makedirs(TICKETS_FOLDER, exist_ok=True)
        filename = f"ticket_{venta.id}.pdf"
        filepath = os.path.join(TICKETS_FOLDER, filename)
        pdf.output(filepath)
        
        return filepath
    
    @staticmethod
    def procesar_venta(session):
        carrito = session.get('carrito', [])
        if not carrito:
            raise ValueError("El carrito está vacío")
        
        try:
            db.session.begin()
            
            total = sum(item['subtotal'] for item in carrito)
            nueva_venta = ProcesoVenta(
                total=total,
                fecha=datetime.datetime.now(),
                estado='completada'
            )
            db.session.add(nueva_venta)
            db.session.flush()
            
            for item in carrito:
                stock = db.session.query(Stock).filter_by(id_galleta=item['galleta_id']).first()
                if not stock:
                    raise ValueError(f"No existe stock para la galleta ID {item['galleta_id']}")
                
                unidades = item.get('unidades', item.get('cantidad', 0))
                if stock.cantidad_galleta < unidades:
                    raise ValueError(f"Stock insuficiente para {item['nombre']}")
                
                detalle = DetalleVenta(
                    venta_id=nueva_venta.id,
                    galleta_id=item['galleta_id'],
                    cantidad=unidades,
                    precio_unitario=item['precio_unitario'],
                    subtotal=item['subtotal'],
                    tipo_venta=item['tipo_venta']
                )
                db.session.add(detalle)
                
                stock.cantidad_galleta -= unidades
            
            db.session.commit()
            
            ticket_path = ProcesoVentaController.generar_ticket(nueva_venta)
            
            session['carrito'] = []
            session.modified = True
            
            return nueva_venta, ticket_path
            
        except Exception as e:
            db.session.rollback()
            raise e