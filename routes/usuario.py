from utils import Blueprint, render_template, redirect, request, login_required, url_for, current_user,flash,abort
import json
from forms import *
from controller import controller_usuario
from funcs import crear_log_user, crear_log_error
usuario_bp = Blueprint('usuario', __name__,  url_prefix='/navegante' ,template_folder='templates')

modales_str = '{"detalles": 0, "editar": 0, "agregar": 0}'  
modales = json.loads(modales_str)  # Convertir a diccionario

@usuario_bp.route('/empleado', methods=['POST','GET'])
@login_required
def mostrar_empleados():
    try:
        if current_user.rol_user != 0:
            abort(404)
     
        form_empleado_obj = form_empleado()
        lista_empleados=controller_usuario.obtener_empleados()
        
        return render_template('pages/page-usuario/emlpeado.html',modales=json.dumps(modales),form_empleado=form_empleado_obj,lista_empleados=lista_empleados)
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash("Error al cargar el panel de usuarios", "danger")
        return redirect('/error')
    
@usuario_bp.route('/agregarEmpleado', methods=['POST'])
@login_required
def agregar_proveedor():
    try:
        if current_user.rol_user != 0:
            abort(404)
        form_empleado_obj = form_empleado(request.form)
        if request.method=='POST'and form_empleado_obj.validate_on_submit():
            if (controller_usuario.agregar_empleado(form_empleado_obj)):
                flash("Empleado agregado con éxito", "success")
            return redirect(url_for('usuario.mostrar_empleados'))
        modales["agregar"]=1
        lista_empleados=controller_usuario.obtener_empleados()
        crear_log_user(current_user.usuario, request.url)
        return render_template('pages/page-usuario/emlpeado.html',modales=json.dumps(modales), form_empleado=form_empleado_obj, lista_empleados=lista_empleados)
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash("Error al cargar el panel de usuarios", "danger")
        return redirect('/error')

@usuario_bp.route('/empleado/detallesEmpleado', methods=['GET'])
@login_required
def detalles_empleado():
    try:
        if current_user.rol_user != 0:
            abort(404)
        form_empleado_obj = form_empleado(request.form)
        lista_empleados=controller_usuario.obtener_empleados()
        empleado_seleccionado=controller_usuario.obtener_empleado_especifico(int(request.args.get('id_emp')))
        if(str(request.args.get('modal'))=='edit'):
            modales["editar"]=1
        else:
            modales["detalles"]=1
        return render_template('pages/page-usuario/emlpeado.html',modales=json.dumps(modales) ,form_empleado=form_empleado_obj,lista_empleados=lista_empleados,emp_sel=empleado_seleccionado)
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash("Error al cargar el panel de usuarios", "danger")
        return redirect('/error')

@usuario_bp.route('/actualizarEmpleado', methods=['POST','GET'])
@login_required
def actualizar_empleado():
    try:
        if current_user.rol_user != 0:
            abort(404)
        form_empleado_obj = form_empleado(request.form)
        controller_usuario.actualizar_empleado(int(request.args.get('id_emp_upd')),form_empleado_obj)
        crear_log_user(current_user.usuario, request.url)
        return redirect(url_for('usuario.mostrar_empleados'))
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash("Error al cargar el panel de usuarios", "danger")
        return redirect('/error')

@usuario_bp.route('/eliminarProveedor', methods=['POST','GET'])
@login_required
def eliminar_proveedor():
    try:
        if current_user.rol_user != 0:
            abort(404)
        crear_log_user(current_user.usuario, request.url)
        controller_usuario.eliminar_proveedor(int(request.args.get('id_prov_del')))
        return redirect(url_for('proveedor.mostrar_proveedores'))
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash("Error al cargar el panel de usuarios", "danger")
        return redirect('/error')

@usuario_bp.route('/reactivarProveedor', methods=['POST','GET'])
def reactivarProveedor():
    try:
        if current_user.rol_user != 0:
            abort(404)
        crear_log_user(current_user.usuario, request.url)
        controller_usuario.reactivar_proveedor(int(request.args.get('id_prov_rea')))
        return redirect(url_for('proveedor.mostrar_proveedores'))
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash("Error al cargar el panel de usuarios", "danger")
        return redirect('/error')



@usuario_bp.after_request
def after_request(response):
    proveedor_seleccionado = ''
    modales["detalles"] = 0
    modales["editar"] = 0
    modales["agregar"] = 0
    return response
