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