from dao import dao_galleta
from cqrs import cqrs_galleta
from models import Galleta
from fpdf import FPDF
from datetime import datetime

def agregar_galleta(form_data, imagen_file):
    if not cqrs_galleta.validar_galleta(form_data):
        return None
    
    return dao_galleta.crear_galleta(
        nombre_galleta=form_data['nombre_galleta'],
        precio_galleta=form_data['precio_galleta'],
        descripcion_galleta=form_data.get('descripcion_galleta', ''),
        imagen_file=imagen_file,
        cantidad_galleta=form_data.get('cantidad_galleta', 0)
    )

def obtener_galletas():
    return dao_galleta.obtener_galletas_activas()

def obtener_galleta(galleta_id):
    return dao_galleta.obtener_galleta_por_id(galleta_id)