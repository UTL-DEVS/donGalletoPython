from utils.db import db
from datetime import datetime

class ResumenVenta(db.Model):
    __tablename__ = 'resumen_ventas'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha_corte = db.Column(db.Date, nullable=False)
    total_ventas = db.Column(db.Integer, nullable=False)
    total_ingresos = db.Column(db.Float, nullable=False)
    ruta_archivo = db.Column(db.String(255), nullable=False)