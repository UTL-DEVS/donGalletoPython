from models import Usuario, Persona, Empleado
from dao import dao_usuario
from funcs import hash

import os
def obtener_empleados():
    return dao_usuario. obtener_empleados()


def agregar_empleado(form_empleado):
    nuevo_persona_prov=Persona()
    nuevo_persona_prov.nombre=str(form_empleado.nombre.data)
    nuevo_persona_prov.primerApellido=str(form_empleado.primer_apellido.data)
    nuevo_persona_prov.segundoApellido=str(form_empleado.segundo_apellido.data)
    nuevo_persona_prov.correo=str(form_empleado.correo.data)
    nuevo_persona_prov.direccion=str(form_empleado.direccion.data)
    nuevo_persona_prov.telefono=str(form_empleado.telefono.data)
    id_persona = dao_usuario.guardar_info_persona(nuevo_persona_prov)
    if(id_persona != None):
        nuevo_us=Usuario()
        nuevo_us.token = '00'
        nuevo_us.usuario=str(form_empleado.nombre_usuario.data)
        nuevo_us.contrasenia=hash(str(form_empleado.contrasenia.data))
        nuevo_us.rol_user=str(form_empleado.rol_user.data)
        nuevo_us.email=str(form_empleado.correo.data)
        nuevo_us.id_persona=(id_persona)
        id_usuario = dao_usuario.guardar_info_usuario(nuevo_us)
        print(f'idusuario registrado {id_usuario}')
        if(id_usuario != None):
            nuevo_em = Empleado()
            nuevo_em.id_usuario = id_usuario
            nuevo_em.id_persona = id_persona
            nuevo_em.sueldo_empleado = float(form_empleado.sueldo.data)
            nuevo_em.dias_laborales = int(form_empleado.dias_laborales.data)
            return dao_usuario.guardar_info_empleado(nuevo_em)
    
def obtener_empleado_especifico(id_empleado):
    return dao_usuario.obtener_empleado_especifico(id_empleado)


def actualizar_empleado(id_empleado, form_empleado):
    emp_sel=dao_usuario.obtener_empleado_especifico(id_empleado)
    emp_sel.id_empleado=id_empleado
    emp_sel.sueldo_empleado= float(form_empleado.sueldo.data)
    emp_sel.dias_laborales=int(form_empleado.dias_laborales.data)
   
    return dao_usuario.guardar_info_empleado(emp_sel)

'''
def eliminar_proveedor(id_empleado):
    prov_eliminar = dao_proveedor.obtener_proveedor_especifico(id_proveedor)
    prov_eliminar.persona.estatus=0
    return cqrs_proveedor.actualizar_proveedor(prov_eliminar)

def reactivar_proveedor(id_proveedor):
    prov_eliminar = dao_proveedor.obtener_proveedor_especifico(id_proveedor)
    prov_eliminar.persona.estatus=1
    return cqrs_proveedor.actualizar_proveedor(prov_eliminar)

'''