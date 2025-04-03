from models import Galleta
from utils.db import db
import base64

def getAllGalletas():
    galletas = Galleta.query.filter_by(activo=1).all()
    
    return galletas

def crear_galleta(nombre_galleta, precio_galleta, descripcion_galleta, imagen_file, cantidad_galleta):
    imagen_base64 = None
    if imagen_file:
        imagen_base64 = base64.b64encode(imagen_file.read()).decode('utf-8')
    
    nueva_galleta = Galleta(
        nombre_galleta=nombre_galleta,
        precio_galleta=precio_galleta,
        descripcion_galleta=descripcion_galleta,
        imagen_galleta=imagen_base64,
        cantidad_galleta=cantidad_galleta
    )
    
    db.session.add(nueva_galleta)
    db.session.commit()
    return nueva_galleta

def obtener_galletas_activas():
    return Galleta.query.filter_by(activo=True).all()

def obtener_galleta_por_id(galleta_id):
    return Galleta.query.get(galleta_id)

def actualizar_stock(galleta_id, cantidad):
    galleta = Galleta.query.get(galleta_id)
    if galleta:
        galleta.cantidad_galleta -= cantidad
        db.session.commit()
        return True
    return False
