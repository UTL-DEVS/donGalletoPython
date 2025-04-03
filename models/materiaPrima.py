from utils.db import db

class MateriaPrima(db.Model):
    __tablename__ = 'materia_prima'
    
    id_materia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_materia = db.Column(db.String(100), nullable=False)
    # si es kilo, costal, o gramos, colocar en gramos
    """
    ejemplo si es un kilo, colocar en el stock 1000
    seria lo equivalente a gramos
    hacer todas las convesiones a gramos en el stock_materia, si es litro a minilitor
    ejemplo si es un litro poner 1000
    si es por pieza colocar la cantidad de piezas
    """
    stock_materia = db.Column(db.Float, nullable=False)
    # Costal, Kilo, Litro, Pieza, Gramos, lata
    unidad_medida_publico = db.Column(db.Integer, nullable=False)
    unidad_medida = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    estatus = db.Column(db.Integer, nullable=False, default=1)

"""
ejemplo si le mete un
"""