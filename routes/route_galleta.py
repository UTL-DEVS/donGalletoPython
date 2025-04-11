# this module is only to galleta crud

from utils import Blueprint, request, render_template, db, flash, redirect, url_for, abort, login_required, current_user
from models import Galleta, Stock
from forms import GalletaForm
import base64
import os
from funcs import crear_log_user, crear_log_error



route_galleta = Blueprint('galleta_route', __name__,  template_folder='templates')

# # Página principal de galletas
# @route_galleta.route('/galleta_home', methods=['GET'])
# @login_required
# def galleta_home():
#     if current_user.rol_user != 0:
#         abort(404)

#     try:
#         crear_log_user(current_user.usuario, request.url)
#         galletas = Galleta.query.all()
#         return render_template('pages/page-galleta/galletas.html', galletas=galletas)
#     except Exception as e:
#         crear_log_error(current_user.usuario, str(e))
#         return redirect('/error')
@route_galleta.route('/galleta_home', methods=['GET', 'POST'])
@login_required
def galleta_home():
    if current_user.rol_user != 0:
        abort(404)

    try:
        crear_log_user(current_user.usuario, request.url)
        form = GalletaForm()

        if form.validate_on_submit():
            imagen = form.imagen_galleta.data

            if imagen:
                imagen_bytes = imagen.read()
                imagen_base64 = base64.b64encode(imagen_bytes).decode('utf-8')
            else:
                imagen_base64 = None

            nueva_galleta = Galleta(
                nombre_galleta=form.nombre_galleta.data,
                precio_galleta=form.precio_galleta.data,
                descripcion_galleta=form.descripcion_galleta.data,
                imagen_galleta=imagen_base64
            )

            db.session.add(nueva_galleta)
            db.session.commit()

            nuevo_stock = Stock(
                id_galleta=nueva_galleta.id_galleta,
                cantidad_galleta=0
            )

            db.session.add(nuevo_stock)
            db.session.commit()

            flash("Galleta agregada correctamente.", "success")
            return redirect(url_for('galleta_route.galleta_home'))

        galletas = Galleta.query.all()
        return render_template('pages/page-galleta/galletas.html', galletas=galletas, form=form)

    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        return redirect('/error')



# # Agregar nueva galleta
# @route_galleta.route('/galleta/agregar', methods=['GET', 'POST'])
# @login_required
# def galleta_agregar():
#     if current_user.rol_user != 0:
#         abort(404)

#     try:
#         crear_log_user(current_user.usuario, request.url)
#         form = GalletaForm()
#         if form.validate_on_submit():
#             imagen = form.imagen_galleta.data  # Obtiene el objeto FileStorage

#             if imagen:  # Verifica si hay una imagen antes de procesarla
#                 imagen_bytes = imagen.read()  # Convierte la imagen a bytes
#                 imagen_base64 = base64.b64encode(imagen_bytes).decode('utf-8')
#             else:
#                 imagen_base64 = None  # Si no hay imagen, guarda None o una por defecto

#             nueva_galleta = Galleta(
#                 nombre_galleta=form.nombre_galleta.data,
#                 precio_galleta=form.precio_galleta.data,
#                 descripcion_galleta=form.descripcion_galleta.data,
#                 imagen_galleta=imagen_base64  # Guarda la imagen en base64
#             )

#             db.session.add(nueva_galleta)
#             db.session.commit()  # Realiza el commit primero para obtener el ID de la galleta

#             # Ahora que tienes el ID de la nueva galleta, lo usas para el stock
#             nuevo_stock = Stock(
#                 id_galleta=nueva_galleta.id_galleta,  # Asigna el id_galleta correctamente
#                 cantidad_galleta=0  # Aquí usas el valor predeterminado o lo tomas del formulario si tienes el campo
#             )
            
#             db.session.add(nuevo_stock)
#             db.session.commit()

#             return redirect(url_for('galleta_route.galleta_home'))

#         return render_template('pages/page-galleta/agregar_galleta.html', form=form)

#     except Exception as e:
#         crear_log_error(current_user.usuario, str(e))
#         return redirect('/error')


# Modificar galleta existente
@route_galleta.route('/galleta/modificar/<int:id>', methods=['GET', 'POST'])
@login_required
def galleta_modificar(id):
    if current_user.rol_user != 0:
        abort(404)

    try:
        crear_log_user(current_user.usuario, request.url)

        galleta = Galleta.query.get_or_404(id)  # Busca la galleta o lanza error 404
        form = GalletaForm(obj=galleta)  # Carga los datos en el formulario

        if form.validate_on_submit():
            galleta.nombre_galleta = form.nombre_galleta.data
            galleta.precio_galleta = form.precio_galleta.data
            galleta.descripcion_galleta = form.descripcion_galleta.data

            # Manejo de imagen
            imagen = form.imagen_galleta.data
            if imagen:  # Si el usuario sube una nueva imagen
                imagen_bytes = imagen.read()
                galleta.imagen_galleta = base64.b64encode(imagen_bytes).decode('utf-8')

            db.session.commit()
            return redirect(url_for('galleta_route.galleta_home'))

        return render_template('pages/page-galleta/modificar_galleta.html', form=form, galleta=galleta)

    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        return redirect('/error')


# Desactivar galleta
@route_galleta.route('/galleta/desactivar/<int:id>')
@login_required
def galleta_desactivar(id):
    if current_user.rol_user != 0:
        abort(404)

    try:
        crear_log_user(current_user.usuario, request.url)

        galleta = Galleta.query.get_or_404(id)  
        galleta.activo = False
        os.system('cls')  # Limpia consola (solo útil en desarrollo)
        print(galleta)
        db.session.commit()
        return redirect(url_for('galleta_route.galleta_home'))

    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        return redirect('/error')


# Activar galleta
@route_galleta.route('/galleta/activar/<int:id>')
@login_required
def galleta_activar(id):
    if current_user.rol_user != 0:
        abort(404)

    try:
        crear_log_user(current_user.usuario, request.url)

        galleta = Galleta.query.get_or_404(id)
        galleta.activo = True
        db.session.commit()
        return redirect(url_for('galleta_route.galleta_home'))

    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        return redirect('/error')