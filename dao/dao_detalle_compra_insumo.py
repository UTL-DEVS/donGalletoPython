from utils import db
from models.compra_insumos import CompraInsumo
from models.compra_insumos import DetalleCompraInsumo
from models.materiaPrima import MateriaPrima

def obetenerDetallesSolicitudes(id_solicitud):
    try:
        insumos = db.session.query(
            DetalleCompraInsumo.id_detalle,
            DetalleCompraInsumo.cantidad, 
            DetalleCompraInsumo.fecha_caducidad,
            DetalleCompraInsumo.precio_unitario,
            MateriaPrima.nombre_materia
        ).select_from(DetalleCompraInsumo)\
        .join(MateriaPrima, DetalleCompraInsumo.id_materia == MateriaPrima.id_materia)\
        .filter(DetalleCompraInsumo.id_compra == id_solicitud)\
        .all()
        return insumos
    except Exception as exception:
        return -1

def agregarDetalleInsumo(solicitudDetalleInsumo):
    try:
        db.session.add(solicitudDetalleInsumo)
        db.session.commit()
        print(solicitudDetalleInsumo.id_detalle)
        return 1
    except Exception as exception:
        return -1
