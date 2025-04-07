from flask import Blueprint, render_template, session, redirect, url_for, flash
from forms.form_cliente import PaqueteForm, PesoForm, PiezaForm
from models.galleta import Galleta
from models.pedido import Pedido
from utils.db import db
from functools import wraps

pedidos_ventas_bp = Blueprint('pedidos_ventas', __name__, template_folder='templates')

def obtener_galletas_activas():
    return Galleta.query.filter_by(activo=True).all()


@pedidos_ventas_bp.route('/ventas/crear-pedido')
def crear_pedido():
    return render_template('pages/pages-ventas/crear_pedido.html',
                         include_template='pages/page-cliente/menu.html')

@pedidos_ventas_bp.route('/ventas/pedido-paquete')
def pedido_paquete():
    galletas = obtener_galletas_activas()
    forms = {galleta.id_galleta: PaqueteForm(id_galleta=galleta.id_galleta) for galleta in galletas}
    return render_template('pages/pages-ventas/pedido_paquete.html',
                         include_template='pages/page-cliente/paquete.html',
                         galletas=galletas,
                         forms=forms,
                         carrito=session.get('carrito', []),
                         total=sum(item['precio']*item['cantidad'] for item in session.get('carrito', [])))

@pedidos_ventas_bp.route('/ventas/pedido-peso')
def pedido_peso():
    galletas = obtener_galletas_activas()
    forms = {galleta.id_galleta: PesoForm(id_galleta=galleta.id_galleta) for galleta in galletas}
    return render_template('pages/pages-ventas/pedido_peso.html',
                         include_template='pages/page-cliente/peso.html',
                         galletas=galletas,
                         forms=forms,
                         carrito=session.get('carrito', []),
                         total=sum(item['precio']*item['cantidad'] for item in session.get('carrito', [])))

@pedidos_ventas_bp.route('/ventas/pedido-unidad')
def pedido_unidad():
    galletas = obtener_galletas_activas()
    forms = {galleta.id_galleta: PiezaForm(id_galleta=galleta.id_galleta) for galleta in galletas}
    return render_template('pages/pages-ventas/pedido_unidad.html',
                         include_template='pages/page-cliente/pedido.html',
                         galletas=galletas,
                         forms=forms,
                         carrito=session.get('carrito', []),
                         total=sum(item['precio']*item['cantidad'] for item in session.get('carrito', [])))

@pedidos_ventas_bp.route('/ventas/pedido-tabla')
def pedido_tabla():
    id_usuario = session.get('usuario_id')
    pedidos = (Pedido.query
               .filter_by(id_usuario=id_usuario)
               .order_by(Pedido.fecha_pedido.desc())
               .all())
    return render_template('pages/pages-ventas/pedido_tabla.html',
                         include_template='pages/page-cliente/tabla_pedido.html',
                         pedidos=pedidos)