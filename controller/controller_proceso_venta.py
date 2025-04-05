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
            pdf.cell(60, 10, detalle.galleta.nombre_galleta, 1, 0)
            pdf.cell(40, 10, detalle.tipo_venta.upper(), 1, 0)
            
            if detalle.tipo_venta == 'unidad':
                pdf.cell(30, 10, f"{detalle.metadata_json.get('cantidad_unidades', 0)} u", 1, 0)
            elif detalle.tipo_venta == 'peso':
                pdf.cell(30, 10, f"{detalle.metadata_json.get('gramos', 0)}g", 1, 0)
            else:
                pdf.cell(30, 10, f"1 paq. ({detalle.metadata_json.get('cantidad_paquetes', 0)}u)", 1, 0)
            
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
    def agregar_al_carrito(session, galleta_id, nombre, precio, cantidad, tipo_venta):
        carrito = session.get('carrito', [])
        
        item_key = f"{galleta_id}_{tipo_venta}"
        item = next((item for item in carrito 
                if f"{item['galleta_id']}_{item['tipo_venta']}" == item_key), None)
        
        if item:
            if tipo_venta == 'unidad':
                item['cantidad'] += cantidad
                item['unidades_equivalentes'] += cantidad
            elif tipo_venta == 'peso':
                item['gramos'] += cantidad
                item['unidades_equivalentes'] += cantidad / 10
            elif tipo_venta == 'paquete':
                item['cantidad_paquetes'] += 1
                item['unidades_equivalentes'] += cantidad  
        else:
            item = {
                'galleta_id': galleta_id,
                'nombre': nombre,
                'precio_unitario': precio,
                'tipo_venta': tipo_venta,
                'cantidad': 0,
                'gramos': 0,
                'cantidad_paquetes': 0,
                'unidades_equivalentes': 0
            }
            
            if tipo_venta == 'unidad':
                item['cantidad'] = cantidad
                item['unidades_equivalentes'] = cantidad
            elif tipo_venta == 'peso':
                item['gramos'] = cantidad
                item['unidades_equivalentes'] = cantidad / 10
            elif tipo_venta == 'paquete':
                item['cantidad_paquetes'] = 1
                item['unidades_equivalentes'] = cantidad
            
            carrito.append(item)
        
        item['subtotal'] = item['unidades_equivalentes'] * precio
        
        session['carrito'] = carrito
        session.modified = True
        return carrito

    @staticmethod
    def procesar_venta(session):
        carrito = session.get('carrito', [])
        if not carrito:
            raise ValueError("El carrito está vacío")
        
        try:
            
            total = sum(item['subtotal'] for item in carrito)
            nueva_venta = ProcesoVenta(
                total=total,
                fecha=datetime.datetime.now(),
                estado='completada'
            )
            db.session.add(nueva_venta)
            db.session.flush()
            
            for item in carrito:
                stock = Stock.query.filter_by(id_galleta=item['galleta_id']).first()
                if not stock:
                    raise ValueError(f"No existe stock para {item['nombre']}")
                
                unidades = item.get('unidades_equivalentes', item.get('cantidad', 0))
                if stock.cantidad_galleta < unidades:
                    raise ValueError(
                        f"Stock insuficiente de {item['nombre']}. "
                        f"Necesitas: {unidades}u, "
                        f"Disponibles: {stock.cantidad_galleta}u"
                    )
            
            for item in carrito:
                stock = Stock.query.filter_by(id_galleta=item['galleta_id']).first()
                unidades = item.get('unidades_equivalentes', item.get('cantidad', 0))
                stock.cantidad_galleta -= unidades
                
                detalle = DetalleVenta(
                    venta_id=nueva_venta.id,
                    galleta_id=item['galleta_id'],
                    cantidad=unidades,
                    precio_unitario=item['precio_unitario'],
                    subtotal=item['subtotal'],
                    tipo_venta=item['tipo_venta'],
                    metadata_json={
                        'cantidad_unidades': item.get('cantidad', 0),
                        'gramos': item.get('gramos', 0),
                        'cantidad_paquetes': item.get('cantidad_paquetes', 0)
                    }
                )
                db.session.add(detalle)
            
            db.session.commit()
            
            ticket_path = ProcesoVentaController.generar_ticket(nueva_venta)
            session['carrito'] = []
            session.modified = True
            
            return nueva_venta, ticket_path
            
        except Exception as e:
            db.session.rollback()
            raise e