from models.ventas import Producto
from utils.db import db
import base64

def crear_producto(nombre, precio, descripcion, imagen_file, cantidad):
    imagen_base64 = None
    if imagen_file:
        imagen_base64 = base64.b64encode(imagen_file.read()).decode('utf-8')
    
    nuevo_producto = Producto(
        nombre=nombre,
        precio=precio,
        descripcion=descripcion,
        imagen=imagen_base64,
        cantidad=cantidad
    )
    
    db.session.add(nuevo_producto)
    db.session.commit()
    return nuevo_producto

def obtener_productos_activos():
    return Producto.query.filter_by(activo=True).all()

def obtener_producto_por_id(producto_id):
    return Producto.query.get(producto_id)