from models.materiaPrima import MateriaPrima
from models.proveedor import Proveedor
from models.receta import Receta
from models.detalle_receta import DetalleReceta
from utils import db

def obtenerInsumos():
    insumos = db.session.query(
        MateriaPrima.id_materia,
        MateriaPrima.nombre_materia, 
        MateriaPrima.stock_materia,
        MateriaPrima.unidad_medida,
        MateriaPrima.cantidad_compra,
        MateriaPrima.precio,
        MateriaPrima.estatus,
        Proveedor.nombre_proveedor
    ).select_from(MateriaPrima)\
    .join(Proveedor, MateriaPrima.id_proveedor == Proveedor.id_proveedor)\
    .filter(MateriaPrima.estatus == 1)\
    .all()
    return insumos

def obtenerInsumosHistorial(fecha):
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
            materiaPrima = MateriaPrima.query.get(solicitud.id_materia)
            unidadMedida = 0
            if solicitud.unidad_medida == 1:
                unidadMedida = 1
            if solicitud.unidad_medida == 3:
                unidadMedida = 1000
            if solicitud.unidad_medida == 4:
                unidadMedida = 1000
            cantidadTotal = (solicitud.stock_materia * solicitud.cantidad_compra) * unidadMedida
            materiaPrima.stock_materia += cantidadTotal
            db.session.add(materiaPrima)
            db.session.commit()
            return 1
        except Exception as exception:
            return -1

def descontarStock(idGalleta, cantidad):
    try:
        receta = db.session.query(Receta).filter_by(id_galleta=idGalleta, estado='1').first()
        lstDetalles = db.session.query(DetalleReceta).filter_by(id_receta=receta.id_receta).all()
        for detalle in lstDetalles:
            materiaPrima = db.session.query(MateriaPrima).filter_by(id_materia=detalle.id_materia).first()  
            descuento = detalle.cantidad_insumo * cantidad
            if materiaPrima.stock_materia < descuento:
                return -3
            materiaPrima.stock_materia = materiaPrima.stock_materia - descuento
            db.session.add(materiaPrima)
            db.session.commit()
        return 1
    except Exception as exception:
        return -1



