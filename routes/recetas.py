from utils import Blueprint, render_template, redirect, flash, db, url_for, request, login_required, current_user
from models import Receta, detalleReceta, MateriaPrima, Galleta
from forms import DetalleRecetaForm, RecetaForm
import os

recetas_bp = Blueprint('receta', __name__, template_folder='templates')

@recetas_bp.route('/receta')
@login_required
def receta_index():
    if current_user.rol_user != 0:
        return redirect('/')
    recetas = Receta.query.all()
    return render_template('/pages/recetas.html', recetas=recetas)


@recetas_bp.route('/receta/<int:id_receta>', methods=['GET', 'POST'])
@login_required
def receta_detalle(id_receta):
    if current_user.rol_user != 0:
        return redirect('/')
    receta = Receta.query.get_or_404(id_receta)  # Cargar la receta por ID
    detalles = detalleReceta.query.filter_by(receta_id=id_receta).all()  # Obtener los detalles de la receta
    form = DetalleRecetaForm()

    detalle_receta_obj = detalleReceta.query.filter_by(receta_id=id_receta).first()
    id_galleta_local = detalle_receta_obj.id_galleta if detalle_receta_obj else None
    if id_galleta_local is None:
        os.system('cls')
        print('nulo')
        return redirect('/receta/agregar')
    nombre_galleta_local = Galleta.query.filter_by(id_galleta=id_galleta_local).first().nombre_galleta
    if request.method == 'POST':
        os.system('cls')
        print('creado')
        # Crear un nuevo detalleReceta si el formulario fue enviado correctamente
        """
        logica para aumentar los insumos receta
        """
        insumo_local = detalleReceta.query.filter_by(receta_id=id_receta, id_materia=form.id_materia.data).first()
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

    return render_template('pages/receta_detalle.html', receta=receta, detalles=detalles, form=form, nombre_galleta=nombre_galleta_local)

@recetas_bp.route('/receta/desactivar/<int:id_receta>')
@login_required
def receta_deactivar(id_receta):
    if current_user.rol_user != 0:
        return redirect('/')
    receta = Receta.query.get_or_404(id_receta)
    receta.estado = '0'
    db.session.commit()
    return redirect('/receta')

@recetas_bp.route('/receta/activar/<int:id_receta>')
@login_required
def receta_activar(id_receta):
    if current_user.rol_user != 0:
        return redirect('/')
    receta = Receta.query.get_or_404(id_receta)
    receta.estado = '1'
    db.session.commit()
    return redirect('/receta')

@recetas_bp.route('/receta/agregar', methods=['GET', 'POST'])
@login_required
def agregar_receta():
    if current_user.rol_user != 0:
        return redirect('/')
    
    form = RecetaForm()
    form.id_galleta.choices = [(g.id_galleta, g.nombre_galleta) for g in Galleta.query.filter_by(activo=True).all()]
    form.id_materia.choices = [(mp.id_materia, mp.nombre_materia) for mp in MateriaPrima.query.all()]
    
    if form.validate_on_submit():
        galleta = Galleta.query.get(form.id_galleta.data)
        
        if not galleta:
            flash('La galleta seleccionada no es válida.', 'danger')
            return redirect(url_for('receta.agregar_receta'))
        
        nueva_receta = Receta(
            nombre_receta=form.nombre_receta.data,
            estado='1'  # La receta comienza activa
        )
        db.session.add(nueva_receta)
        db.session.commit()
        
        nuevo_detalle = detalleReceta(
            receta_id=nueva_receta.id_receta,
            id_galleta=galleta.id_galleta,
            id_materia=form.id_materia.data,
            cantidad_insumo=form.cantidad_insumo.data
        )
        db.session.add(nuevo_detalle)
        
        galleta.activo = False  # Cambiar el estado de la galleta
        db.session.commit()
        
        flash('Receta agregada exitosamente.', 'success')
        return redirect(url_for('receta.receta_index'))
    
    return render_template('pages/agregar_receta.html', form=form)


@recetas_bp.route('/receta/<int:id_receta>/detalle/eliminar/<int:id_detalle>', methods=['POST'])
@login_required
def eliminar_detalle(id_receta, id_detalle):
    if current_user.rol_user != 0:
        return redirect('/')
    receta = Receta.query.get_or_404(id_receta)
    detalles = detalleReceta.query.filter_by(receta_id=id_receta).all()

    if len(detalles) == 1:
        flash('No se puede eliminar el único detalle de la receta.', 'danger')
        return redirect(url_for('receta.receta_detalle', id_receta=id_receta))

    detalle = detalleReceta.query.get_or_404(id_detalle)
    db.session.delete(detalle)
    db.session.commit()
    flash('Detalle eliminado exitosamente.', 'success')
    return redirect(url_for('receta.receta_detalle', id_receta=id_receta))


    