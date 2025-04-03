from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from controller.controller_cliente import ClienteController
from forms.form_cliente import PaqueteForm, PesoForm, PiezaForm
from models.pedido import Pedido 
from utils.db import db
from models.galleta import Galleta
from datetime import  timedelta
from models.usuario import Usuario
from werkzeug.security import generate_password_hash ,check_password_hash

cliente_bp = Blueprint('cliente', __name__, template_folder='templates')

@cliente_bp.route('/cliente')
def inicio():
    return render_template('pages/page-cliente/inicio.html')

@cliente_bp.route('/cliente/menu')
def menu():
    galletas = ClienteController.obtener_galletas_activas()
    forms = {galleta.id_galleta: PaqueteForm(id_galleta=galleta.id_galleta) for galleta in galletas}
    return render_template('pages/page-cliente/menu.html',
                        carrito=session.get('carrito', []),
                        total=ClienteController.calcular_total(),
                        galletas=galletas,
                        forms=forms)

@cliente_bp.route('/paquete')
def paquete():
    galletas = ClienteController.obtener_galletas_activas()
    forms = {galleta.id_galleta: PaqueteForm(id_galleta=galleta.id_galleta) for galleta in galletas}
    return render_template('pages/page-cliente/paquete.html',
                        carrito=session.get('carrito', []),
                        total=ClienteController.calcular_total(),
                        galletas=galletas,
                        forms=forms)

@cliente_bp.route('/peso')
def peso():
    galletas = ClienteController.obtener_galletas_activas()
    forms = {galleta.id_galleta: PesoForm(id_galleta=galleta.id_galleta) for galleta in galletas}
    return render_template('pages/page-cliente/peso.html',
                        carrito=session.get('carrito', []),
                        total=ClienteController.calcular_total(),
                        galletas=galletas,
                        forms=forms)

@cliente_bp.route('/piezas')
def piezas():
    galletas = ClienteController.obtener_galletas_activas()
    forms = {galleta.id_galleta: PiezaForm(id_galleta=galleta.id_galleta) for galleta in galletas}
    return render_template('pages/page-cliente/pedido.html',
                        carrito=session.get('carrito', []),
                        total=ClienteController.calcular_total(),
                        galletas=galletas,
                        forms=forms)

@cliente_bp.route('/agregar/<int:id_galleta>', methods=['POST'])
def agregar(id_galleta):

    galleta = db.session.query(
        Galleta.id_galleta,
        Galleta.nombre_galleta,
        Galleta.precio_galleta,
        Galleta.imagen_galleta,
        Galleta.descripcion_galleta,
        Galleta.cantidad_galleta,
        Galleta.fecha_creacion,
        Galleta.activo
    ).filter_by(id_galleta=id_galleta, activo=True).first()
    
    
    if not galleta:
        flash("Producto no encontrado", "error")
        return redirect(url_for('cliente.menu'))

    tipo_pedido = request.form.get('tipo_pedido')
    form_data = request.form

    try:
        precio = ClienteController.calcular_precio(tipo_pedido, id_galleta, form_data)
        cantidad = form_data.get('cantidad', 1)
        ClienteController.agregar_al_carrito(
            id_galleta, 
            galleta.nombre_galleta, 
            precio, 
            cantidad, 
            tipo_pedido
        )
        flash("Producto agregado al carrito", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
    
    return redirect(request.referrer or url_for('cliente.menu'))

@cliente_bp.route('/eliminar-del-carrito/<int:index>')
def eliminar_del_carrito(index):
    producto = ClienteController.eliminar_del_carrito(index)
    if producto:
        flash(f"Se eliminó {producto['nombre']} del carrito", "success")
    else:
        flash("Índice no válido", "error")
    return redirect(request.referrer or url_for('cliente.piezas'))

@cliente_bp.route('/realizar-pedido', methods=['POST'])
def realizar_pedido():
    try:
        id_usuario = session.get('id_usuario', 1)
        pedido = ClienteController.realizar_pedido(id_usuario)
        flash(f"Pedido #{pedido.id_pedido} realizado con éxito!", "success")
        return redirect(url_for('cliente.confirmacion_pedido', id_pedido=pedido.id_pedido))
    except Exception as e:
        flash(str(e), "error")
        return redirect(url_for('cliente.piezas'))

@cliente_bp.route('/confirmacion-pedido/<int:id_pedido>')
def confirmacion_pedido(id_pedido):
    
    pedido = Pedido.query.get_or_404(id_pedido)
    return render_template('pages/page-cliente/tabla_pedido.html', pedido=pedido)


@cliente_bp.route('/vaciar-carrito', methods=['GET'])
def vaciar_carrito():
    if ClienteController.vaciar_carrito():
        flash("Carrito vaciado correctamente", "success")
    else:
        flash("El carrito ya estaba vacío", "info")
    return redirect(url_for('cliente.piezas'))


@cliente_bp.route('/mis-pedidos')
def mis_pedidos():
    id_usuario = session.get('id_usuario', 1)
    pedidos = (Pedido.query
        .filter_by(id_usuario=id_usuario)
        .order_by(Pedido.fecha_pedido.desc())
        .options(db.joinedload(Pedido.detalles))
        .all())
    for pedido in pedidos:
        for detalle in pedido.detalles:
            if not hasattr(detalle, 'galleta'):
                detalle.galleta = Galleta.query.get(detalle.id_galleta)
    
    return render_template('pages/page-cliente/tabla_pedido.html', pedidos=pedidos)

MAX_INTENTOS = 3
TIEMPO_LIMITE = timedelta(hours=1) 
@cliente_bp.route('/perfil-cliente', methods=['GET', 'POST'])
def perfil_cliente():

    #if 'usuario_id' not in session:
        #flash('Por favor, inicia sesión para acceder a esta página.', 'danger')
        #return redirect('/login')

    #usuario_id = session['usuario_id']
    #usuario = Usuario.query.get(usuario_id)

    if request.method == 'POST':
        contrasena_actual = request.form['contrasena_actual']
        nueva_contrasena = request.form['nueva_contrasena']

        # Verificar que la contraseña actual es correcta
        #if not check_password_hash(usuario.contrasenia, contrasena_actual):
            #flash('La contraseña actual es incorrecta.', 'danger')
            #return redirect('/perfil_cliente')
        
        # Actualizar la contraseña
        #usuario.contrasenia = generate_password_hash(nueva_contrasena)
        #db.session.commit()

        flash('Contraseña cambiada exitosamente.', 'success')
        return redirect('/perfil')  # O a donde desees redirigir después de cambiar la contraseña

    return render_template('pages/page-cliente/perfil_cliente.html')