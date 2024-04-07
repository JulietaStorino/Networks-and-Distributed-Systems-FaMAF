import socket
from constants import *
import os
import os.path
from base64 import b64encode

def parse_and_run(self, line):
    """
    Parsea los datos del pedido y ejecuta el comando correspondiente.
    """
    pass

def get_file_listing(self):
    """
    Obtiene la lista de archivos disponibles en el servidor.
    """
    if not os.path.exists(self.directory): # FALTA: Ver que pasa si el directorio no existe
        # Si el directorio no existe envía un mensaje de error
        mensaje = f'{FILE_NOT_FOUND} {error_messages[FILE_NOT_FOUND]}\r\n'
        mensaje = b64encode(mensaje)
        self.socket.send(mensaje)
        return
    # Lista los archivos del directorio
    files = os.listdir(self.directory)
    # Redacta la confirmación de lectura
    mensaje = f'{CODE_OK} {error_messages[CODE_OK]}\r\n'
    # Redacta la lista de archivos
    for file in files:
        mensaje += file + b'\r\n'
    mensaje += b'\r\n'
    mensaje = b64encode(mensaje)
    self.socket.send(mensaje)

def get_metadata(self, FILENAME):
    """
    Retorna el tamaño del archivo.
    """
    pass

def get_slice(self, FILENAME, OFFSET, SIZE):
    """
    Retorna un fragmento del archivo.
    """
    pass

def quit(self):
    """
    Cierra la conexión.
    """
    pass