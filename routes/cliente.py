from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from controller.controller_cliente import ClienteController
from forms.form_cliente import PaqueteForm, PesoForm, PiezaForm, CambioContrasenaForm
from models.pedido import Pedido 
from utils.db import db
from utils import abort, logout_user, login_required, current_user
import hashlib
from models.galleta import Galleta
from datetime import  timedelta
from models.usuario import Usuario
from werkzeug.security import generate_password_hash ,check_password_hash
from funcs import crear_log_error, crear_log_user


cliente_bp = Blueprint('cliente', __name__, template_folder='templates')

@cliente_bp.route('/cliente')
@login_required
def inicio():
    if current_user.rol_user != 1:
        abort(404)
    
    try:
        crear_log_user(current_user.usuario, request.url)
        return render_template('pages/page-cliente/inicio.html')
    except Exception as e:
        crear_log_error(current_user.usuario,str(e))
        abort(404)

@cliente_bp.route('/cliente/menu')
@login_required
def menu():
    if current_user.rol_user != 1:
        abort(404)
        crear_log_user(current_user.usuario, request.url)
        galletas = ClienteController.obtener_galletas_activas()
        forms = {galleta.id_galleta: PaqueteForm(id_galleta=galleta.id_galleta) for galleta in galletas}
        return render_template('pages/page-cliente/menu.html',
                        carrito=session.get('carrito', []),
                        total=ClienteController.calcular_total(),
                        galletas=galletas,
                        forms=forms)

@cliente_bp.route('/paquete')
@login_required
def paquete():
    if current_user.rol_user != 1:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)
        galletas = ClienteController.obtener_galletas_activas()
        forms = {galleta.id_galleta: PaqueteForm(id_galleta=galleta.id_galleta) for galleta in galletas}
        return render_template('pages/page-cliente/paquete.html',
                        carrito=session.get('carrito', []),
                        total=ClienteController.calcular_total(),
                        galletas=galletas,
                        forms=forms)
    except Exception as e:
        crear_log_error(current_user.usuario,str(e))
        abort(404)

@cliente_bp.route('/peso')
@login_required
def peso():
    if current_user.rol_user != 1:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)
        galletas = ClienteController.obtener_galletas_activas()
        forms = {galleta.id_galleta: PesoForm(id_galleta=galleta.id_galleta) for galleta in galletas}
        return render_template('pages/page-cliente/peso.html',
                        carrito=session.get('carrito', []),
                        total=ClienteController.calcular_total(),
                        galletas=galletas,
                        forms=forms)
    except Exception as e:
        crear_log_error(current_user.usuario,str(e))
        abort(404)
        
    

@cliente_bp.route('/piezas')
@login_required
def piezas():
    if current_user.rol_user != 1:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)
        galletas = ClienteController.obtener_galletas_activas()
        forms = {galleta.id_galleta: PiezaForm(id_galleta=galleta.id_galleta) for galleta in galletas}
        return render_template('pages/page-cliente/pedido.html',
                        carrito=session.get('carrito', []),
                        total=ClienteController.calcular_total(),
                        galletas=galletas,
                        forms=forms)
    except Exception as e:
        crear_log_error(current_user.usuario,str(e))
        abort(404)
        

@cliente_bp.route('/agregar/<int:id_galleta>', methods=['POST'])
@login_required
def agregar(id_galleta):
    if current_user.rol_user != 1:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)
        galleta = db.session.query(
        Galleta.id_galleta,
        Galleta.nombre_galleta,
        Galleta.precio_galleta,
        Galleta.imagen_galleta,
        Galleta.descripcion_galleta,
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
    except Exception as e:
        crear_log_error(current_user.usuario,str(e))
        abort(404)

@cliente_bp.route('/eliminar-del-carrito/<int:index>')
@login_required
def eliminar_del_carrito(index):
    if current_user.rol_user != 1:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)
        producto = ClienteController.eliminar_del_carrito(index)
        if producto:
            flash(f"Se eliminó {producto['nombre']} del carrito", "success")
        else:
            flash("Índice no válido", "error")
        return redirect(request.referrer or url_for('cliente.piezas'))
    except Exception as e:
        crear_log_error(current_user.usuario,str(e))
        abort(404)

@cliente_bp.route('/realizar-pedido', methods=['POST'])
@login_required
def realizar_pedido():
    if current_user.rol_user != 1:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)
        id_usuario = session.get('id_usuario', 1)
        pedido = ClienteController.realizar_pedido(id_usuario)
        flash(f"Pedido #{pedido.id_pedido} realizado con éxito!", "success")
        return redirect(url_for('cliente.mis_pedidos', id_pedido=pedido.id_pedido))
    except Exception as e:
        crear_log_error(current_user.usuario,str(e))
        abort(404)


@cliente_bp.route('/vaciar-carrito', methods=['GET'])
@login_required
def vaciar_carrito():
    if current_user.rol_user != 1:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)
        if ClienteController.vaciar_carrito():
            flash("Carrito vaciado correctamente", "success")
        else:
            flash("El carrito ya estaba vacío", "info")
        return redirect(url_for('cliente.piezas'))
    except Exception as e:
        crear_log_error(current_user.usuario,str(e))
        abort(404)


@cliente_bp.route('/mis-pedidos')
@login_required
def mis_pedidos():
    if current_user.rol_user != 1:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)
        
        id_usuario = session['usuario_id']
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
    except Exception as e:
        crear_log_error(current_user.usuario,str(e))
        abort(404)





def hash_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode('utf-8')).hexdigest()

@cliente_bp.route('/perfil-cliente', methods=['GET', 'POST'])
@login_required
def perfil_cliente():
    try:
        crear_log_user(current_user.usuario, request.url)
        if 'usuario_id' not in session:
            return redirect('/login')

        usuario_id = session['usuario_id']
        usuario = Usuario.query.get(usuario_id)
        form = CambioContrasenaForm()  # Creamos la instancia del formulario

        if form.validate_on_submit():  # Verificamos si el formulario es válido
            contrasena_actual = form.contrasena_actual.data
            nueva_contrasena = form.nueva_contrasena.data

            # Verificar que la contraseña actual es correcta
            if usuario.contrasenia != hash_contrasena(contrasena_actual):
                flash('La contraseña actual es incorrecta.', 'danger')
                return redirect('/cliente/perfil-cliente')

            # Encriptar la nueva contraseña y actualizarla en la base de datos
            usuario.contrasenia = hash_contrasena(nueva_contrasena)
            db.session.commit()

            flash('Contraseña cambiada exitosamente.', 'success')
            return redirect('perfil-cliente')

        return render_template('pages/page-cliente/perfil_cliente.html', usuario=usuario, form=form)
    except Exception as e:
        crear_log_error(current_user.usuario,str(e))
        abort(404)

@cliente_bp.route('/actualizar-pedido', methods=['POST'])
def actualizarPedido():
    pedido = request.get_json()
    resultado = ClienteController.actualizarPedido(pedido)
    if resultado != 1:
        return {
            'codigo': 'error',
            'mensaje': 'Ocurrio un error al procesar el pedido!'
        }
    else:
        return {
            'codigo': 'success',
            'mensaje': 'El pedido se proceso correctamente!'
        }