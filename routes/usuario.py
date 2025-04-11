from utils import Blueprint, render_template, redirect, request, login_required, url_for, current_user,flash,abort
import json
from forms import form_edit_emp, form_empleado
from controller import controller_usuario
from funcs import crear_log_user, crear_log_error
usuario_bp = Blueprint('usuario', __name__,  url_prefix='/navegante' ,template_folder='templates')

modales_str = '{"detalles": 0, "editar": 0, "agregar": 0}'  
modales = json.loads(modales_str)  # Convertir a diccionario

@usuario_bp.route('/empleado', methods=['POST','GET'])
def mostrar_empleados():
        form_empleado_obj = form_empleado()
        lista_empleados=controller_usuario.obtener_empleados()
        
        return render_template('pages/page-usuario/emlpeado.html',modales=json.dumps(modales),form_empleado=form_empleado_obj,lista_empleados=lista_empleados)
    
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
                crear_log_user(current_user.usuario, request.url)
            return redirect('/navegante/empleado')
        modales["agregar"]=1
        lista_empleados=controller_usuario.obtener_empleados()
        return render_template('pages/page-usuario/emlpeado.html',modales=json.dumps(modales), form_empleado=form_empleado_obj, lista_empleados=lista_empleados)
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash("Error al cargar el panel de usuarios", "danger")
        return redirect('/navegante/empleado')

@usuario_bp.route('/empleado/detallesEmpleado', methods=['GET'])
@login_required
def detalles_empleado():
    try:
        if current_user.rol_user != 0:
            abort(404)
        form_empleado_obj = form_empleado(request.form)
        form_emp_edit = form_edit_emp(request.form)
        lista_empleados=controller_usuario.obtener_empleados()
        empleado_seleccionado=controller_usuario.obtener_empleado_especifico(int(request.args.get('id_emp')))
        if(str(request.args.get('modal'))=='edit'):
            modales["editar"]=1
        else:
            modales["detalles"]=1
        return render_template('pages/page-usuario/emlpeado.html',modales=json.dumps(modales),form_emp_edit=form_emp_edit ,form_empleado=form_empleado_obj,lista_empleados=lista_empleados,emp_sel=empleado_seleccionado)
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash("Error al cargar el panel de usuarios", "danger")
        return redirect('/navegante/empleado')

@usuario_bp.route('/empleado/actualizarEmpleado', methods=['POST','GET'])
@login_required
def actualizar_empleado():
    try:
        if current_user.rol_user != 0:
            abort(404)
        form = form_empleado()
        form_empleado_obj = form_edit_emp(request.form)
        id_emp=int(request.args.get('id_emp_upd'))
        if request.method == 'POST' and form_empleado_obj.validate_on_submit():
            controller_usuario.actualizar_empleado(id_emp,form_empleado_obj)
            crear_log_user(current_user.usuario, request.url)
            flash("Datos de usuario actualizados", "success")
            return redirect('/navegante/empleado')
        modales["editar"]=1
        lista_empleados=controller_usuario.obtener_empleados()
        emp= controller_usuario.obtener_empleado_especifico(id_emp)
        return render_template('pages/page-usuario/emlpeado.html',modales=json.dumps(modales), form_empleado=form, form_emp_edit=form_empleado_obj, lista_empleados=lista_empleados,emp_sel=emp)
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash("Error al cargar el panel de usuarios", "danger")
        return redirect('/navegante/empleado')

@usuario_bp.route('/empleado/eliminarEmpleado', methods=['POST','GET'])
@login_required
def eliminar_empleado():
    try:
        if current_user.rol_user != 0:
            abort(404)
        empleado_seleccionado=controller_usuario.obtener_empleado_especifico(int(request.args.get('id_emp_del')))
        if(empleado_seleccionado.usuario.id == current_user.id):
            flash("No puedes desactivar tu propio usuario", "warning")
            return redirect('/navegante/empleado')
        controller_usuario.eliminar_empleado(empleado_seleccionado.id_empleado)
        crear_log_user(current_user.usuario, request.url)
        return redirect('/navegante/empleado')
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash("Error al cargar el panel de usuarios", "danger")
        return redirect('/navegante/empleado')

@usuario_bp.route('/empleado/reactivarEmpleado', methods=['POST','GET'])
def reactivarProveedor():
    print(f'reactivando us')
    try:
        if current_user.rol_user != 0:
            abort(404)
        crear_log_user(current_user.usuario, request.url)
        controller_usuario.reactivar_empleado(int(request.args.get('id_emp_rea')))
        return redirect('/navegante/empleado')
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash("Error al cargar el panel de usuarios", "danger")
        return redirect('/navegante/empleado')



@usuario_bp.after_request
def after_request(response):
    modales["detalles"] = 0
    modales["editar"] = 0
    modales["agregar"] = 0
    return response
