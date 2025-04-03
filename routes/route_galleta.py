# this module is only to galleta crud

from utils import Blueprint, request, render_template, db, flash, redirect, url_for
from models import Galleta, Stock
from forms import GalletaForm
import base64
import os


route_galleta = Blueprint('galleta_route', __name__,  template_folder='templates')

@route_galleta.route('/galleta_home', methods=['GET'])
def galleta_home():
    galletas = Galleta.query.all()
    return render_template('pages/page-galleta/galletas.html', galletas=galletas)

@route_galleta.route('/galleta/agregar', methods=['GET', 'POST'])
def galleta_agregar():
    form = GalletaForm()
    if form.validate_on_submit():
        imagen = form.imagen_galleta.data  # Obtiene el objeto FileStorage

        if imagen:  # Verifica si hay una imagen antes de procesarla
            imagen_bytes = imagen.read()  # Convierte la imagen a bytes
            imagen_base64 = base64.b64encode(imagen_bytes).decode('utf-8')
        else:
            imagen_base64 = None  # Si no hay imagen, guarda None o una por defecto

        nueva_galleta = Galleta(
            nombre_galleta=form.nombre_galleta.data,
            precio_galleta=form.precio_galleta.data,
            descripcion_galleta=form.descripcion_galleta.data,
            imagen_galleta=imagen_base64  # Guarda la imagen en base64
        )

        db.session.add(nueva_galleta)
        db.session.commit()  # Realiza el commit primero para obtener el ID de la galleta

        # Ahora que tienes el ID de la nueva galleta, lo usas para el stock
        nuevo_stock = Stock(
            id_galleta=nueva_galleta.id_galleta,  # Asigna el id_galleta correctamente
            cantidad_galleta=0  # Aquí usas el valor predeterminado o lo tomas del formulario si tienes el campo
        )
        
        db.session.add(nuevo_stock)
        db.session.commit()

        return redirect(url_for('galleta_route.galleta_home'))

    return render_template('pages/page-galleta/agregar_galleta.html', form=form)


@route_galleta.route('/galleta/modificar/<int:id>', methods=['GET', 'POST'])
def galleta_modificar(id):
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

@route_galleta.route('/galleta/desactivar/<int:id>')
def galleta_desactivar(id):
    galleta = Galleta.query.get_or_404(id)  
    galleta.activo = False
    os.system('cls')
    print(galleta)
    db.session.commit()
    return redirect(url_for('galleta_route.galleta_home'))

@route_galleta.route('/galleta/activar/<int:id>')
def galleta_activar(id):
    galleta = Galleta.query.get_or_404(id)
    galleta.activo = True
    db.session.commit()
    return redirect(url_for('galleta_route.galleta_home'))