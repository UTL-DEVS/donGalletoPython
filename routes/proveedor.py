from flask import Blueprint, render_template,request,render_template_string
import json
from forms import *
from models import Proveedor
from controller import controller_proveedor

proveedor_bp = Blueprint('proveedor', __name__,url_prefix='/proveedor', template_folder='templates')

@proveedor_bp.route('/')
def mostrar_proveedores():
    form_proveedor_obj = form_proveedor()
    form_persona_obj = form_persona()
    lista_proveedores=controller_proveedor.obtener_proveedores()

    return render_template('pages/proveedor.html',form_persona=form_persona_obj,form_proveedor=form_proveedor_obj,lista_proveedores=lista_proveedores)

@proveedor_bp.route('/detallesProveedor', methods=['GET'])
def detalles_proveedor():
    proveedor_seleccionado=controller_proveedor.obtener_proveedor_especifico(int(request.args.get('id_prov')))
    return json.dumps(proveedor_seleccionado.to_dict())

@proveedor_bp.route('/actualizarProveedor', methods=['POST'])
def actualizar_proveedor():
    form_proveedor_obj = form_proveedor()
    form_persona_obj = form_persona(request.form)
    lista_proveedores=controller_proveedor.obtener_proveedores()
    if request.method=='POST':
        controller_proveedor.actualizar_proveedor(int(request.args.get('id_prov_upd')),form_persona_obj)
    return render_template('pages/proveedor.html',form_persona=form_persona_obj,form_proveedor=form_proveedor_obj,lista_proveedores=lista_proveedores)



@proveedor_bp.route('/proveedor/agregar')
def agregar_proveedor():
    form_proveedor = form_proveedor()
    form_persona = form_persona()
    if form_persona.validate_on_submit():
       print('N')
    return render_template('pages/proveedor.html')