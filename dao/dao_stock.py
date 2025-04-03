from utils import db
from flask import jsonify
from models.produccion import Produccion
from models.galleta import Galleta
from models.Stock import Stock
from models.detalle_produccion import DetalleProduccion
from datetime import date

def obtenerStock():
    stock = db.session.query(
        Galleta.id_galleta,
        Galleta.nombre_galleta,
        Stock.cantidad_galleta,
        Stock.maximo_galleta,
        Stock.minimo_galleta
    ).select_from(Galleta)\
    .join(Stock, Galleta.id_galleta == Stock.id_galleta)\
    .all()
    return stock

def agregarStock(nuevoStock):
    try:
        stock = Stock.query.get(nuevoStock.id_galleta)
        if stock:
            stock.cantidad_galleta += nuevoStock.cantidad_galleta
        db.session.commit()
        return 1
    except Exception as exception:
        return -1