from utils import db
from models.compra_insumos import CompraInsumo

def obetenerSolicitudesPendientes():
    try:
        insumos = db.session.query(
            CompraInsumo.id_compra_insumo,
            CompraInsumo.fecha_compra, 
            CompraInsumo.total,
            CompraInsumo.estatus
        ).select_from(CompraInsumo)\
        .filter(CompraInsumo.estatus == 0)\
        .all()
        return insumos
    except Exception as exception:
        return -1

def obetenerSolicitudesAceptadas():
    try:
        insumos = db.session.query(
            CompraInsumo.id_compra_insumo,
            CompraInsumo.fecha_compra, 
            CompraInsumo.total,
            CompraInsumo.estatus
        ).select_from(CompraInsumo)\
        .filter(CompraInsumo.estatus == 1)\
        .all()
        return insumos
    except Exception as exception:
        return -1

def solicitarInsumo(solicitudInsumo):
    try:
        db.session.add(solicitudInsumo)
        db.session.commit()
        return solicitudInsumo.id_compra_insumo
    except Exception as exception:
        return -1

def aceptarSolicitudInsumo(id_solicitud):
    try:
        solicitud = CompraInsumo.query.filter(CompraInsumo.id_compra_insumo == id_solicitud).first()
        if solicitud != None:
            solicitud.estatus = 1
            db.session.add(solicitud)
            db.session.commit()
            return 1
    except Exception as exception:
        return -1