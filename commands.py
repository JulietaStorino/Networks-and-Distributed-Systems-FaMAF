import socket
from constants import *
import os
import os.path

def validate_args(args, expected, connection):
    """
    Verifica si la cantidad de argumentos es la esperada.
    """
    if args != expected:
        mensaje = f'{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}\r\n'
        connection.socket.send(mensaje.encode("ascii"))
        return False
    return True

def parse_and_run(connection, line):
    """
    Parsea los datos del pedido y ejecuta el comando correspondiente.
    """
    parts = line.split()
    if len(parts) == 0:
        return
    command = parts[0]
    args = parts[1:]

    if command == "get_file_listing":
        if validate_args(len(args), 0, connection):
            return get_file_listing(connection)

    elif command == "get_metadata":
        if validate_args(len(args), 1, connection):
            filename = parts[1]
            return get_metadata(connection, filename)
    
    elif command == "get_slice":
        if validate_args(len(args), 3, connection) and parts[2].isdigit() and parts[3].isdigit():
            filename = parts[1]
            offset = int(parts[2])
            size = int(parts[3])
            return get_slice(connection, filename, offset, size)

    elif command == "quit":
        if validate_args(len(args), 0, connection):
            return quit(connection)

    else:
        mensaje = f'{INVALID_COMMAND} {error_messages[INVALID_COMMAND]}\r\n'
        connection.socket.send(mensaje.encode("ascii"))

    return

def get_file_listing(connection):
    """
    Obtiene la lista de archivos disponibles en el servidor.
    """
    if not os.path.exists(connection.directory): # FALTA: Ver que pasa si el directorio no existe
        # Si el directorio no existe envía un mensaje de error
        mensaje = f'{FILE_NOT_FOUND} {error_messages[FILE_NOT_FOUND]}\r\n'
        connection.socket.send(mensaje.encode("ascii"))
        return
    # Lista los archivos del directorio
    try:
        files = os.listdir(connection.directory)
    except:
        mensaje = f'{INTERNAL_ERROR} {error_messages[INTERNAL_ERROR]}\r\n'
        connection.socket.send(mensaje.encode("ascii"))
        return
    # Redacta la confirmación de lectura
    mensaje = f'{CODE_OK} {error_messages[CODE_OK]}\r\n'
    # Redacta la lista de archivos
    for file in files:
        mensaje += f"{file} {EOL}"
    mensaje += f"{EOL}"
    connection.socket.send(mensaje.encode("ascii"))

def get_metadata(connection, FILENAME):#~implementar
    """
    Retorna el tamaño del archivo.
    """
    # Verifica si el directorio especificado por la conexión existe
    if not os.path.exists(connection.directory):
        # Si el directorio no existe envía un mensaje de error
        mensaje = f'{FILE_NOT_FOUND} {error_messages[FILE_NOT_FOUND]}\r\n'
        connection.socket.send(mensaje.encode("ascii"))
        return
    
    # Lista los archivos del directorio
    try:
        files = os.listdir(connection.directory)
    except:
        mensaje = f'{INTERNAL_ERROR} {error_messages[INTERNAL_ERROR]}\r\n'
        connection.socket.send(mensaje.encode("ascii"))
        return

    # Verifica si el archivo solicitado existe
    for file in files:
        if file == FILENAME:
            # Obtiene el tamaño del archivo
            try:
                size = os.path.getsize(file)
            except:
                mensaje = f'{INTERNAL_ERROR} {error_messages[INTERNAL_ERROR]}\r\n'
                connection.socket.send(mensaje.encode("ascii"))
                return
            mensaje = f'{CODE_OK} {error_messages[CODE_OK]}\r\n'
            mensaje += f'{size}\r\n'

            # Codifica el mensaje en base64 y lo envía
            connection.socket.send(mensaje.encode("ascii"))
            return
        
    # Si el archivo no existe envía un mensaje de error
    mensaje = f'{FILE_NOT_FOUND} {error_messages[FILE_NOT_FOUND]}\r\n'
    connection.socket.send(mensaje.encode("ascii"))

def get_slice(connection, FILENAME, OFFSET, SIZE):
    """
    Retorna un fragmento del archivo.
    """
    mensaje = f'{INTERNAL_ERROR} {error_messages[INTERNAL_ERROR]}\r\n'
    connection.socket.send(mensaje.encode("ascii"))
    return

def quit(connection):
    """
    Cierra la conexión.
    """
    connection.quit = True
    mensaje = f'{CODE_OK} {error_messages[CODE_OK]}\r\n'
    connection.socket.send(mensaje.encode("ascii"))
    return