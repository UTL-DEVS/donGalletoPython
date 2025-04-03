from models import Usuario, Persona, Empleado
from utils import db

import os
def obtener_empleados():
    empleados = Empleado.query.join(Persona).join(Usuario).filter(Persona.estatus != 0, Usuario.rol_user != 1).all()
    return empleados

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


def agregar_proveedor(form_proveedor,form_persona):
    nuevo_persona_prov=Persona()
    nuevo_persona_prov.nombre=str(form_persona.nombre.data)
    nuevo_persona_prov.primerApellido=str(form_persona.primer_apellido.data)
    nuevo_persona_prov.segundoApellido=str(form_persona.segundo_apellido.data)
    nuevo_persona_prov.correo=str(form_persona.correo.data)
    nuevo_persona_prov.direccion=str(form_persona.direccion.data)
    nuevo_persona_prov.telefono=str(form_persona.telefono.data)
    id_persona = cqrs_proveedor.agregar_persona_proveedor(nuevo_persona_prov)
    
    if(id_persona != None):
        nuevo_prov=Proveedor()
        nuevo_prov.nombre_proveedor=str(form_proveedor.nombre_proveedor.data)
        nuevo_prov.id_persona=(id_persona)
        return cqrs_proveedor.agregar_proveedor(nuevo_prov)
    else:
        return False'''