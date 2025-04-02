from models import Usuario, Persona, Empleado
from dao import dao_usuario
from utils import db

import os
def obtener_empleados():
    return dao_usuario. obtener_empleados()


def agregar_empleado(form_usuario, form_empleado, form_persona):
    nuevo_persona_prov=Persona()
    nuevo_persona_prov.nombre=str(form_persona.nombre.data)
    nuevo_persona_prov.primerApellido=str(form_persona.primer_apellido.data)
    nuevo_persona_prov.segundoApellido=str(form_persona.segundo_apellido.data)
    nuevo_persona_prov.correo=str(form_usuario.correo.data)
    nuevo_persona_prov.direccion=str(form_persona.direccion.data)
    nuevo_persona_prov.telefono=str(form_persona.telefono.data)
    id_persona = dao_usuario.guardar_info_persona(nuevo_persona_prov)
    if(id_persona != None):
        nuevo_us=Usuario()
        nuevo_us.usuario=str(form_usuario.nombre_usuario.data)
        nuevo_us.contrasenia=str(form_usuario.contrasenia.data)
        nuevo_us.rol_user=str(form_usuario.rol_user.data)
        nuevo_us.email=str(form_usuario.correo.data)
        nuevo_us.id_persona=(id_persona)
        id_usuario = dao_usuario.guardar_info_usuario(nuevo_us)
        if(id_usuario != None):
            nuevo_em = Empleado()
            nuevo_em.id_usuario = id_usuario
            nuevo_em.id_persona = id_persona
            nuevo_em.sueldo_empleado = float(form_empleado.sueldo.data)
    

'''def obtener_proveedor_especifico(id_proveedor):
    return dao_proveedor.obtener_proveedor_especifico(id_proveedor)

def actualizar_proveedor(id_proveedor, form_persona):
    prov_sel=dao_proveedor.obtener_proveedor_especifico(id_proveedor)
    prov_sel.id_proveedor=id_proveedor
    prov_sel.persona.nombre=str(form_persona.nombre.data)
    prov_sel.persona.primerApellido=str(form_persona.primer_apellido.data)
    prov_sel.persona.segundoApellido=str(form_persona.segundo_apellido.data)
    prov_sel.persona.correo=str(form_persona.correo.data)
    prov_sel.persona.direccion=str(form_persona.direccion.data)
    prov_sel.persona.telefono=str(form_persona.telefono.data)
    return cqrs_proveedor.actualizar_proveedor(prov_sel)

def eliminar_proveedor(id_proveedor):
    prov_eliminar = dao_proveedor.obtener_proveedor_especifico(id_proveedor)
    prov_eliminar.persona.estatus=0
    return cqrs_proveedor.actualizar_proveedor(prov_eliminar)

def reactivar_proveedor(id_proveedor):
    prov_eliminar = dao_proveedor.obtener_proveedor_especifico(id_proveedor)
    prov_eliminar.persona.estatus=1
    return cqrs_proveedor.actualizar_proveedor(prov_eliminar)

'''