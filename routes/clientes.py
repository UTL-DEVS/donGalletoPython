from flask import Blueprint, render_template, request, redirect, url_for, session
from models.galleta import Galleta

cliente_bp = Blueprint('cliente', __name__, template_folder='templates')

@cliente_bp.route('/cliente')
def cliente():
    return render_template('pages/page-cliente/inicio.html')

@cliente_bp.route('/cliente/menu')
def menu():
    return render_template('pages/page-cliente/menu.html')


@cliente_bp.route('/pedido')
def pedido():
    carrito = session.get('carrito', [])
    total = sum(item["precio_galleta"] * item["cantidad"] for item in carrito)
    galletas = Galleta.query.filter_by(estatus=1).all() 
    return render_template("pages/page-cliente/pedido.html", carrito=carrito, total=total , galletas=galletas)

