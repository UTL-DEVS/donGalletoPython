from utils.db import db
from datetime import datetime

class GastoOperacion(db.Model):
    __tablename__ = 'gasto_operacion'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    id_usuario = db.Column(db.Integer, nullable=False)  # FK a usuario que lo registró
