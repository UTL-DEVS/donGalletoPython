from utils import Blueprint, render_template, redirect, flash, db, url_for, request
from models import Receta, detalleReceta, MateriaPrima
from forms import DetalleRecetaForm
import os

recetas_bp = Blueprint('receta', __name__, template_folder='templates')

@recetas_bp.route('/receta')
def receta_index():
    recetas = Receta.query.all()
    return render_template('/pages/recetas.html', recetas=recetas)


@recetas_bp.route('/receta/<int:id_receta>', methods=['GET', 'POST'])
def receta_detalle(id_receta):
    receta = Receta.query.get_or_404(id_receta)  # Cargar la receta por ID
    detalles = detalleReceta.query.filter_by(receta_id=id_receta).all()  # Obtener los detalles de la receta
    form = DetalleRecetaForm()

    if request.method == 'POST':
        os.system('cls')
        print('creado')
        # Crear un nuevo detalleReceta si el formulario fue enviado correctamente
        id_galleta_local = detalleReceta.query.filter_by(receta_id=id_receta).first().id_galleta
        
        """
        logica para aumentar los insumos receta
        """
        insumo_local = detalleReceta.query.filter_by(receta_id=id_receta).first()
        if not insumo_local:
            nuevo_detalle = detalleReceta(
                receta_id=id_receta,  # Asignar la receta correspondiente
                id_galleta=id_galleta_local,  # Asignar la galleta seleccionada
                id_materia=form.id_materia.data,  # Asignar la materia prima seleccionada
                cantidad_insumo=form.cantidad_insumo.data  # Asignar la cantidad
            )
            db.session.add(nuevo_detalle)  # Agregar el nuevo detalle a la base de datos
        else:
            insumo_local.cantidad_insumo += form.cantidad_insumo.data  # Aumentar la cantidad
            db.session.merge(insumo_local) 
        db.session.commit()
        return redirect(url_for('receta.receta_detalle', id_receta=id_receta))

    return render_template('pages/receta_detalle.html', receta=receta, detalles=detalles, form=form)

@recetas_bp.route('/receta/desactivar/<int:id_receta>')
def receta_deactivar(id_receta):
    receta = Receta.query.get_or_404(id_receta)
    receta.estado = '0'
    db.session.commit()
    return redirect('/receta')

@recetas_bp.route('/receta/activar/<int:id_receta>')
def receta_activar(id_receta):
    receta = Receta.query.get_or_404(id_receta)
    receta.estado = '1'
    db.session.commit()
    return redirect('/receta')

