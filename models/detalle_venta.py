from utils.db import db

class DetalleVenta(db.Model):
    __tablename__ = 'DetalleVenta'
    
    id_detalle_venta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('Venta.id_venta'), nullable=False)
    id_galleta = db.Column(db.Integer, db.ForeignKey('Galleta.id_galleta'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    tipo_venta = db.Column(db.Integer, nullable=False)
    
    galleta = db.relationship('Galleta', backref=db.backref('DetalleVenta', uselist=False))
