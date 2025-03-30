from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user
from sqlalchemy import text
from utils.db import db
#from connection.config import db
import json

pedido_bp = Blueprint('pedido', __name__, template_folder='templates')

@pedido_bp.route('/')
@login_required
def listar_pedidos():
    if current_user.rol == 'admin':
        pedidos = db.session.execute(text("SELECT * FROM ventas WHERE tipoVenta = 'WEB'")).fetchall()
    else:
        pedidos = db.session.execute(text("SELECT * FROM ventas WHERE tipoVenta = 'WEB' AND descripcion LIKE :cliente"), {"cliente": f"%ClienteID:{current_user.id}%"}).fetchall()
    return render_template('pages/page-pedidos/listado.html', pedidos=pedidos)

@pedido_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_pedido():
    galletas = db.session.execute(text("SELECT * FROM galletas")).fetchall()

    if request.method == 'POST':
        galleta_ids = request.form.getlist('galleta_id')
        cantidades = request.form.getlist('cantidad')
        fecha_recoleccion = request.form.get('fecha_recoleccion')

        descripcion = " | ".join([
            f"GalletaID:{gid},Cantidad:{cant}" for gid, cant in zip(galleta_ids, cantidades)
        ])
        descripcion += f" | ClienteID:{current_user.id}"

        db.session.execute(text("""
            INSERT INTO ventas (descripcion, total, fecha, hora, tipoVenta, desde_web, procesado_en_caja, fecha_recoleccion)
            VALUES (:descripcion, 0, CURDATE(), CURTIME(), 'WEB', TRUE, FALSE, :fecha_recoleccion)
        """), {
            "descripcion": descripcion,
            "fecha_recoleccion": fecha_recoleccion
        })

        db.session.commit()
        flash("Pedido registrado correctamente. Esperando aprobación del administrador.")
        return redirect(url_for('pedido.listar_pedidos'))

    return render_template('pages/page-pedidos/nuevo.html', galletas=galletas)

@pedido_bp.route('/aceptar/<int:pedido_id>')
@login_required
def aceptar_pedido(pedido_id):
    if current_user.rol != 'admin':
        flash("No tienes permisos para esta acción.")
        return redirect(url_for('pedido.listar_pedidos'))

    venta = db.session.execute(text("SELECT * FROM ventas WHERE id_venta = :id"), {"id": pedido_id}).fetchone()

    if not venta:
        flash("Pedido no encontrado.")
        return redirect(url_for('pedido.listar_pedidos'))

    descripcion = venta.descripcion
    galletas = []

    for parte in descripcion.split("|"):
        parte = parte.strip()
        if parte.startswith("GalletaID"):
            datos = parte.split(",")
            gid = int(datos[0].split(":")[1])
            cantidad = int(datos[1].split(":")[1])
            galletas.append((gid, cantidad))

    for galleta_id, cantidad in galletas:
        insumos = db.session.execute(text("""
            SELECT ri.insumo_id, ri.cantidad * :cantidad AS total
            FROM receta_insumo ri
            JOIN receta r ON r.id = ri.receta_id
            WHERE r.galleta_id = :gid
        """), {"cantidad": cantidad, "gid": galleta_id}).fetchall()

        insumos_json = [
            {"id_insumo": insumo.insumo_id, "cantidad_descontar": insumo.total} for insumo in insumos
        ]

        db.session.execute(text("""
            CALL agregarGalletasYDescontarInsumos(:gid, :cantidad, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 30 DAY), :insumos, 0)
        """), {
            "gid": galleta_id,
            "cantidad": cantidad,
            "insumos": json.dumps(insumos_json)
        })

    db.session.execute(text("""
        UPDATE ventas SET procesado_en_caja = FALSE WHERE id_venta = :id
    """), {"id": pedido_id})

    db.session.commit()
    flash("Pedido aceptado. Agregado para procesamiento en caja.")
    return redirect(url_for('pedido.listar_pedidos'))
