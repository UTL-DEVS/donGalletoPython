from utils import Blueprint, render_template, redirect, flash, url_for, request, login_required, current_user
import json
from forms import *
from controller import controller_proveedor

proveedor_bp = Blueprint('proveedor', __name__,url_prefix='/proveedor', template_folder='templates')

modales_str = '{"detalles": 0, "editar": 0, "agregar": 0}'  
modales = json.loads(modales_str)  # Convertir a diccionario

@proveedor_bp.route('/', methods=['POST','GET'])
@login_required
def mostrar_proveedores():
    form_proveedor_obj = form_proveedor(request.form)
    form_persona_obj = form_persona(request.form)
    lista_proveedores=controller_proveedor.obtener_proveedores()
    if current_user.rol_user != 0 :
        return redirect('/login')
    return render_template('pages/proveedor.html',modales=json.dumps(modales),form_persona=form_persona_obj,form_proveedor=form_proveedor_obj,lista_proveedores=lista_proveedores)

@proveedor_bp.route('/detallesProveedor', methods=['GET'])
@login_required
def detalles_proveedor():
    if current_user.rol_user != 0 :
        return redirect('/login')
    form_proveedor_obj = form_proveedor(request.form)
    form_persona_obj = form_persona(request.form)
    lista_proveedores=controller_proveedor.obtener_proveedores()
    proveedor_seleccionado=controller_proveedor.obtener_proveedor_especifico(int(request.args.get('id_prov')))
    if(str(request.args.get('modal'))=='edit'):
        modales["editar"]=1
    else:
        modales["detalles"]=1
   
    return render_template('pages/proveedor.html',modales=json.dumps(modales),form_proveedor=form_proveedor_obj ,form_persona=form_persona_obj,lista_proveedores=lista_proveedores,prov_sel=proveedor_seleccionado)
    # return redirect(url_for('proveedor.mostrar_proveedores'))
    #return json.dumps(proveedor_seleccionado.to_dict())

@proveedor_bp.route('/actualizarProveedor', methods=['POST','GET'])
@login_required
def actualizar_proveedor():
    if current_user.rol_user != 0 :
        return redirect('/login')
    form_persona_obj = form_persona()
    controller_proveedor.actualizar_proveedor(int(request.args.get('id_prov_upd')),form_persona_obj)
    
    return redirect(url_for('proveedor.mostrar_proveedores'))

@proveedor_bp.route('/eliminarProveedor', methods=['POST','GET'])
@login_required
def eliminar_proveedor():
    if current_user.rol_user != 0 :
        return redirect('/login')
    controller_proveedor.eliminar_proveedor(int(request.args.get('id_prov_del')))
    
    return redirect(url_for('proveedor.mostrar_proveedores'))

@proveedor_bp.route('/reactivarProveedor', methods=['POST','GET'])
@login_required
def reactivarProveedor():
    if current_user.rol_user != 0 :
        return redirect('/login')
    controller_proveedor.reactivar_proveedor(int(request.args.get('id_prov_rea')))
    return redirect(url_for('proveedor.mostrar_proveedores'))



@proveedor_bp.route('/agregarProveedor', methods=['POST'])
@login_required
def agregar_proveedor():
    if current_user.rol_user != 0 :
        return redirect('/login')
    form_proveedor_obj = form_proveedor(request.form)
    form_persona_obj = form_persona()
    if request.method=='POST' and form_proveedor_obj.validate_on_submit():
        controller_proveedor.agregar_proveedor(form_proveedor_obj,form_persona_obj)
        return redirect(url_for('proveedor.mostrar_proveedores'))
    else:
        modales["agregar"]=1
        lista_proveedores=controller_proveedor.obtener_proveedores()
 
    return render_template('pages/proveedor.html',modales=json.dumps(modales),form_persona=form_persona_obj,form_proveedor=form_proveedor_obj,lista_proveedores=lista_proveedores)


@proveedor_bp.after_request
def after_request(response):
    proveedor_seleccionado=''
    modales["detalles"]=0
    modales["editar"]=0
    modales["agregar"]=0
    return response

