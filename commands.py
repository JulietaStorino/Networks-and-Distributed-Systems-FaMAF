import socket
from constants import *


def parse_and_run(self, line):
    """
    Parsea los datos del pedido y ejecuta el comando correspondiente.
    """
    pass

def get_file_listing(self):
    """
    Obtiene la lista de archivos disponibles en el servidor.
    """
    pass

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