from dao import dao_proveedor
import os
def obtener_proveedores():
    return dao_proveedor.obtener_proveedores()

def obtener_proveedor_especifico(id_proveedor):
    return dao_proveedor.obtener_proveedor_especifico(id_proveedor)

def actualizar_proveedor(id_proveedor, form_persona):
    prov_sel=dao_proveedor.obtener_proveedor_especifico(id_proveedor)
    prov_sel.id_proveedor=id_proveedor
    prov_sel.nombre=str(form_persona.nombre)
    prov_sel.primerApellido=str(form_persona.primer_apellido)
    prov_sel.segundoApellido=str(form_persona.segundo_apellido)
    prov_sel.correo=str(form_persona.correo)
    prov_sel.direccion=str(form_persona.direccion)
    prov_sel.telefono=str(form_persona.telefono)
    return dao_proveedor.actualizar_proveedor(prov_sel)