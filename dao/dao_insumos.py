from models.materiaPrima import MateriaPrima
from models.proveedor import Proveedor
from utils import db

def obtenerInsumos():
    insumos = db.session.query(
        MateriaPrima.id_materia,
        MateriaPrima.nombre_materia, 
        MateriaPrima.stock_materia,
        MateriaPrima.unidad_medida,
        MateriaPrima.precio,
        MateriaPrima.estatus,
        Proveedor.nombre_proveedor
    ).select_from(MateriaPrima)\
    .join(Proveedor, MateriaPrima.id_proveedor == Proveedor.id_proveedor)\
    .filter(MateriaPrima.estatus == 1)\
    .all()
    return insumos

def actualizarStock(solicitud):
        try:
            print('dao:')
            materiaPrima = MateriaPrima.query.get(solicitud.id_materia)
            materiaPrima.stock_materia += solicitud.stock_materia
            db.session.add(materiaPrima)
            db.session.commit()
            return 1
        except Exception as exception:
            return -1
        