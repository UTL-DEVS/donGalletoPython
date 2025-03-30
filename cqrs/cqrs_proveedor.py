from dao import dao_proveedor

def actualizar_proveedor(prov_sel):
    return dao_proveedor.actualizar_proveedor(prov_sel)    

def agregar_persona_proveedor(persona_prov):
    return dao_proveedor.agregar_persona_proveedor(persona_prov)

def agregar_proveedor(prov):
    return dao_proveedor.agregar_proveedor(prov)