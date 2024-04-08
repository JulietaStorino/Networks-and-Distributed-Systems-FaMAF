import socket
from constants import *
import os
import os.path
from base64 import b64encode

def parse_and_run(connection, line):
    """
    Parsea los datos del pedido y ejecuta el comando correspondiente.
    """
    pass

def get_file_listing(connection):
    """
    Obtiene la lista de archivos disponibles en el servidor.
    """
    if not os.path.exists(connection.directory): # FALTA: Ver que pasa si el directorio no existe
        # Si el directorio no existe envía un mensaje de error
        mensaje = f'{FILE_NOT_FOUND} {error_messages[FILE_NOT_FOUND]}\r\n'
        mensaje = b64encode(mensaje)
        connection.socket.send(mensaje)
        return
    # Lista los archivos del directorio
    try:
        files = os.listdir(connection.directory)
    except:
        mensaje = f'{INTERNAL_ERROR} {error_messages[INTERNAL_ERROR]}\r\n'
        mensaje = b64encode(mensaje)
        connection.socket.send(mensaje)
        return
    # Redacta la confirmación de lectura
    mensaje = f'{CODE_OK} {error_messages[CODE_OK]}\r\n'
    # Redacta la lista de archivos
    for file in files:
        mensaje += file + b'\r\n'
    mensaje += b'\r\n'
    mensaje = b64encode(mensaje)
    connection.socket.send(mensaje)

def get_metadata(connection, FILENAME):#~implementar
    """
    Retorna el tamaño del archivo.
    """
    # Verifica si el directorio especificado por la conexión existe
    if not os.path.exists(connection.directory):
        # Si el directorio no existe envía un mensaje de error
        mensaje = f'{FILE_NOT_FOUND} {error_messages[FILE_NOT_FOUND]}\r\n'
        mensaje = b64encode(mensaje)
        connection.socket.send(mensaje)
        return
    
    # Lista los archivos del directorio
    try:
        files = os.listdir(connection.directory)
    except:
        mensaje = f'{INTERNAL_ERROR} {error_messages[INTERNAL_ERROR]}\r\n'
        mensaje = b64encode(mensaje)
        connection.socket.send(mensaje)
        return

    # Verifica si el archivo solicitado existe
    for file in files:
        if file == FILENAME:
            # Obtiene el tamaño del archivo
            try:
                size = os.path.getsize(file)
            except:
                mensaje = f'{INTERNAL_ERROR} {error_messages[INTERNAL_ERROR]}\r\n'
                mensaje = b64encode(mensaje)
                connection.socket.send(mensaje)
                return
            mensaje = f'{CODE_OK} {error_messages[CODE_OK]}\r\n'
            mensaje += f'{size}\r\n'

            # Codifica el mensaje en base64 y lo envía
            mensaje = b64encode(mensaje)
            connection.socket.send(mensaje)
            return
        
    # Si el archivo no existe envía un mensaje de error
    mensaje = f'{FILE_NOT_FOUND} {error_messages[FILE_NOT_FOUND]}\r\n'

def get_slice(connection, FILENAME, OFFSET, SIZE):
    """
    Retorna un fragmento del archivo.
    """
    pass

def quit(connection):
    """
    Cierra la conexión.
    """
    connection.quit = True
    connection.socket.close()
    return