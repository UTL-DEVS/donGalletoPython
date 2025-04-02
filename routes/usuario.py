from utils import Blueprint, render_template, redirect, request, login_required, url_for, current_user
import json
from forms import *
from controller import controller_usuario
usuario_bp = Blueprint('usuario', __name__,  url_prefix='/usuario' ,template_folder='templates')

modales_str = '{"detalles": 0, "editar": 0, "agregar": 0}'  
modales = json.loads(modales_str)  # Convertir a diccionario

@usuario_bp.route('/empleado', methods=['POST','GET'])
@login_required
def mostrar_empleados():
    if current_user.rol_user != 0 :
        return redirect('/login')
    form_usuario_obj = form_usuario(request.form)
    form_persona_obj = form_persona(request.form)
    form_empleado_obj = form_empleado(request.form)
    lista_empleados=controller_usuario.obtener_empleados()
    
    return render_template('pages/page-usuario/emlpeado.html',modales=json.dumps(modales),form_persona=form_persona_obj,form_usuario=form_usuario_obj,form_empleado=form_empleado_obj,lista_empleados=lista_empleados)

@usuario_bp.route('/agregarEmpleado', methods=['POST'])
@login_required
def agregar_proveedor():
    form_usuario_obj = form_usuario(request.form)
    form_persona_obj = form_persona(request.form)
    form_empleado_obj = form_empleado(request.form)
    if request.method=='POST' and form_usuario_obj.validate_on_submit():
        controller_usuario.agregar_empleado(form_usuario_obj, form_empleado_obj, form_persona_obj)
        return redirect(url_for('usuario.mostrar_empleados'))
    modales["agregar"]=1
    lista_empleados=controller_usuario.obtener_empleados()
    return render_template('pages/page-usuario/emlpeado.html',modales=json.dumps(modales),form_persona=form_persona_obj,form_usuario=form_usuario_obj,form_empleado=form_empleado_obj,lista_empleados=lista_empleados)


@usuario_bp.route('/empleado/detallesEmpleado', methods=['GET'])
@login_required
def detalles_proveedor():
    if current_user.rol_user != 0 :
        return redirect('/login')
    form_usuario_obj = form_proveedor(request.form)
    form_persona_obj = form_persona(request.form)
    lista_empleados=controller_usuario.obtener_proveedores()
    proveedor_seleccionado=controller_usuario.obtener_proveedor_especifico(int(request.args.get('id_prov')))
    if(str(request.args.get('modal'))=='edit'):
        modales["editar"]=1
    else:
        modales["detalles"]=1
    return render_template('pages/proveedor.html',modales=json.dumps(modales),form_proveedor=form_usuario_obj ,form_persona=form_persona_obj,lista_empleados=lista_empleados,prov_sel=proveedor_seleccionado)
    # return redirect(url_for('proveedor.mostrar_proveedores'))
    #return json.dumps(proveedor_seleccionado.to_dict())

@usuario_bp.route('/actualizarProveedor', methods=['POST','GET'])
@login_required
def actualizar_proveedor():
    form_persona_obj = form_persona()
    controller_usuario.actualizar_proveedor(int(request.args.get('id_prov_upd')),form_persona_obj)
    return redirect(url_for('proveedor.mostrar_proveedores'))

@usuario_bp.route('/eliminarProveedor', methods=['POST','GET'])
@login_required
def eliminar_proveedor():
    controller_usuario.eliminar_proveedor(int(request.args.get('id_prov_del')))
    return redirect(url_for('proveedor.mostrar_proveedores'))

@usuario_bp.route('/reactivarProveedor', methods=['POST','GET'])
@login_required
def reactivarProveedor():
    controller_usuario.reactivar_proveedor(int(request.args.get('id_prov_rea')))
    return redirect(url_for('proveedor.mostrar_proveedores'))





@usuario_bp.after_request
def after_request(response):
    proveedor_seleccionado=''
    modales["detalles"]=0
    modales["editar"]=0
    modales["agregar"]=0
    return response

