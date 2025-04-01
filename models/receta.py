from utils.db import db
class Receta(db.Model):
    
    __tablename__ = 'receta'
    id_receta = db.Column(db.Integer, primary_key=True)
    nombre_receta = db.Column(db.String(100), nullable=False, unique=True)
    estado = db.Column(db.String(1), nullable=False)
    detalles = db.relationship('detalleReceta', backref='receta', lazy=True)
    
class detalleReceta(db.Model):
    id_detalle_receta = db.Column(db.Integer, primary_key=True)
    cantidad_insumo = db.Column(db.Float, nullable=False)
    id_galleta = db.Column(db.Integer, db.ForeignKey('galletas.id_galleta'), nullable=False)
    id_materia = db.Column(db.Integer, db.ForeignKey('materia_prima.id_materia'), nullable=False)
    galleta = db.relationship('Galleta', backref='detalles', lazy=True)
    # Relacion con MateriaPrima
    materia_prima = db.relationship('MateriaPrima', backref='detalles', lazy=True)
    # Relacion con Receta
    receta_id = db.Column(db.Integer, db.ForeignKey('receta.id_receta'), nullable=False)