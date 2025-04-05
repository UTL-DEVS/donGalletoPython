from utils import db
from datetime import datetime

class CompraInsumo(db.Model):

    __tablename__ = 'compra_insumo'
    id_compra_insumo = db.Column(db.Integer, primary_key=True)
    fecha_compra = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    estatus = db.Column(db.Integer, nullable=False, default=0)  # 0: pendiente, 1: aceptada

    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario', backref='compras', lazy=True)
    # Relación a detalles
    detalles = db.relationship('DetalleCompraInsumo', backref='compra', lazy=True)

class DetalleCompraInsumo(db.Model):
    __tablename__ = 'detalle_compra'
    id_detalle = db.Column(db.Integer, primary_key=True)
    id_compra = db.Column(db.Integer, db.ForeignKey('compra_insumo.id_compra_insumo'), nullable=False)
    id_materia = db.Column(db.Integer, db.ForeignKey('materia_prima.id_materia'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)  # En gramos, mililitros o piezas, según unidad
    precio_unitario = db.Column(db.Float, nullable=False)
    materia_prima = db.relationship('MateriaPrima', backref='detalle_compra')
