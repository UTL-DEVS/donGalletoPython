from dao import dao_proveedor
import os
def obtener_proveedores():
    return dao_proveedor.obtener_proveedores()

def obtener_proveedor_especifico(id_proveedor):
    return dao_proveedor.obtener_proveedor_especifico(id_proveedor)