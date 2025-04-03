from flask import Blueprint, render_template,request, redirect,url_for, current_user, login_required, abort, flash
import json
from forms import *
from controller import controller_usuario
from funcs import crear_log_user, crear_log_error

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario', template_folder='templates')

modales_str = '{"detalles": 0, "editar": 0, "agregar": 0}'  
modales = json.loads(modales_str)  # Convertir a diccionario

@usuario_bp.route('/empleado', methods=['POST', 'GET'])
@login_required
def mostrar_empleado():
    if current_user.rol_user != 0:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)

        form_usuario_obj = form_usuario(request.form)
        form_persona_obj = form_persona(request.form)
        form_empleado_obj = form_empleado(request.form)
        lista_empleados = controller_usuario.obtener_empleados()

        print(f'empleados: {lista_empleados[0]}')

        return render_template('pages/page-usuario/emlpeado.html',
                               modales=json.dumps(modales),
                               form_persona=form_persona_obj,
                               form_usuario=form_usuario_obj,
                               form_empleado=form_empleado_obj,
                               lista_empleados=lista_empleados)
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        return redirect('/error')

@usuario_bp.route('/empleado/detallesEmpleado', methods=['GET'])
@login_required
def detalles_proveedor():
    if current_user.rol_user != 0:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)

        form_usuario_obj = form_proveedor(request.form)
        form_persona_obj = form_persona(request.form)
        lista_empleados = controller_usuario.obtener_proveedores()
        proveedor_seleccionado = controller_usuario.obtener_proveedor_especifico(int(request.args.get('id_prov')))
        if str(request.args.get('modal')) == 'edit':
            modales["editar"] = 1
        else:
            modales["detalles"] = 1
        return render_template('pages/proveedor.html',
                               modales=json.dumps(modales),
                               form_proveedor=form_usuario_obj,
                               form_persona=form_persona_obj,
                               lista_empleados=lista_empleados,
                               prov_sel=proveedor_seleccionado)
        # return redirect(url_for('proveedor.mostrar_proveedores'))
        #return json.dumps(proveedor_seleccionado.to_dict())
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        return redirect('/error')

@usuario_bp.route('/actualizarProveedor', methods=['POST', 'GET'])
@login_required
def actualizar_proveedor():
    if current_user.rol_user != 0:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)
        form_persona_obj = form_persona()
        controller_usuario.actualizar_proveedor(int(request.args.get('id_prov_upd')), form_persona_obj)
        return redirect(url_for('proveedor.mostrar_proveedores'))
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        return redirect('/error')

@usuario_bp.route('/eliminarProveedor', methods=['POST', 'GET'])
@login_required
def eliminar_proveedor():
    if current_user.rol_user != 0:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)
        controller_usuario.eliminar_proveedor(int(request.args.get('id_prov_del')))
        return redirect(url_for('proveedor.mostrar_proveedores'))
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        return redirect('/error')

@usuario_bp.route('/reactivarProveedor', methods=['POST', 'GET'])
@login_required
def reactivarProveedor():
    if current_user.rol_user != 0:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)
        controller_usuario.reactivar_proveedor(int(request.args.get('id_prov_rea')))
        return redirect(url_for('proveedor.mostrar_proveedores'))
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        return redirect('/error')

@usuario_bp.route('/agregarProveedor', methods=['POST'])
@login_required
def agregar_proveedor():
    if current_user.rol_user != 0:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)

        form_usuario_obj = form_proveedor(request.form)
        form_persona_obj = form_persona()
        if request.method == 'POST' and form_usuario_obj.validate_on_submit():
            controller_usuario.agregar_proveedor(form_usuario_obj, form_persona_obj)
            return redirect(url_for('proveedor.mostrar_proveedores'))
        else:
            modales["agregar"] = 1
            lista_empleados = controller_usuario.obtener_proveedores()
            return render_template('pages/proveedor.html',
                                   modales=json.dumps(modales),
                                   form_persona=form_persona_obj,
                                   form_proveedor=form_usuario_obj,
                                   lista_empleados=lista_empleados)
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        return redirect('/error')

@usuario_bp.after_request
def after_request(response):
    proveedor_seleccionado = ''
    modales["detalles"] = 0
    modales["editar"] = 0
    modales["agregar"] = 0
    return response
