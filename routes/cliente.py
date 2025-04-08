from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from controller.controller_cliente import ClienteController
from forms.form_cliente import PaqueteForm, PesoForm, PiezaForm, CambioContrasenaForm
from models.pedido import Pedido 
from utils.db import db
from utils import abort, login_required, current_user
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
    print(current_user.id)
    if current_user.rol_user != 1:
        return redirect('/')
    galletas = ClienteController.obtener_galletas_activas()
    return render_template('pages/page-cliente/inicio.html', galletas=galletas)

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
        id_usuario = session.get('usuario_id')
        pedido = ClienteController.realizar_pedido(id_usuario)
        flash(f"Pedido #{pedido.id_pedido} realizado con éxito!", "success")
        return redirect(url_for('cliente.mis_pedidos', id_pedido=pedido.id_pedido))


@cliente_bp.route('/vaciar-carrito', methods=['GET'])
def vaciar_carrito():
        if ClienteController.vaciar_carrito():
            flash("Carrito vaciado correctamente", "success")
        else:
            flash("El carrito ya estaba vacío", "info")
        return redirect(url_for('cliente.piezas'))


@cliente_bp.route('/mis-pedidos')

def mis_pedidos():
        id_usuario = session['usuario_id']
        print(id_usuario)
        print('hola desde pedidos')
        print(type(id_usuario))
        pedidos = (Pedido.query
            .filter_by(id_usuario=id_usuario)
            .order_by(Pedido.fecha_pedido.desc())
            .options(db.joinedload(Pedido.detalles))
            .all())
        print(pedidos)
        for pedido in pedidos:
            for detalle in pedido.detalles:
                if not hasattr(detalle, 'galleta'):
                    detalle.galleta = Galleta.query.get(detalle.id_galleta)
    
        return render_template('pages/page-cliente/tabla_pedido.html', pedidos=pedidos)





def hash_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode('utf-8')).hexdigest()

@cliente_bp.route('/perfil-cliente', methods=['GET', 'POST'])
def perfil_cliente():
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