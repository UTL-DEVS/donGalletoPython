import os
from pathlib import Path
from datetime import datetime
actual = os.getcwd()
def crear_log_user(usuario, accion):
    # Creamos el archivo log.txt en la carpeta logs
    archivo = Path(actual) / 'logs'
    archivo_text = open(archivo / 'logs_monitoreo.txt', 'a')
    # Escribimos el mensaje en el archivo log
    archivo_text.write(f'Fecha: {datetime.now()} - Usuario: {usuario} - Accion: {accion}\n')
    
    
    


def crear_log_error(usuario, accion):
    # Creamos el archivo log.txt en la carpeta logs
    archivo = Path(actual) / 'logs'
    archivo_text = open(archivo / 'logs_error.txt', 'a')
    # Escribimos el mensaje en el archivo log, con fecha now
    archivo_text.write(f'Fecha: {datetime.now()} - Usuario: {usuario} - Accion: {accion}\n')
    

def log_producto(usuario, entidad, entidad_id, accion, detalle=""):
    """
    Guarda un log unificado en logs_producto.txt.

    - usuario: nombre de usuario que hace el cambio
    - entidad: nombre del modulp o modelo (ej: 'insumo', 'galleta', etc.)
    - entidad_id: ID del objeto afectado
    - accion: 'creación', 'modificación', 'eliminación'
    - detalle: texto adicional (ej: campo modificado o valores)
    """
    try:
        carpeta_logs = Path(actual) / 'logs'
        carpeta_logs.mkdir(exist_ok=True)

        with open(carpeta_logs / 'logs_producto.txt', 'a', encoding='utf-8') as archivo:
            archivo.write(
                f'[{datetime.now()}] - Usuario: {usuario} - {entidad.capitalize()} ID: {entidad_id} - Acción: {accion.upper()} - {detalle}\n'
            )
    except Exception as e:
        print(f"[ERROR AL REGISTRAR LOG] {e}")