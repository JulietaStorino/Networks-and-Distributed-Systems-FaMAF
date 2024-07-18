import socket
from constants import *
import os
import os.path
from base64 import b64encode

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
        if len(args) != 0:
            mensaje = f'{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}\r\n'
            mensaje = (mensaje.encode('utf-8'))
            connection.socket.send(mensaje)
            return 
        
        return get_file_listing(connection)
    
    elif command == "get_metadata":
        if len(args) != 1:
            mensaje = f'{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}\r\n'
            mensaje = (mensaje.encode('utf-8'))
            connection.socket.send(mensaje)
            return 
        filename = parts[1]
        return get_metadata(connection, filename)
    
    elif command == "get_slice":
        if len(args) != 3 or not (parts[2].isdigit() and parts[3].isdigit   ()):
            mensaje = f'{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}\r\n'
            mensaje = (mensaje.encode('utf-8'))
            connection.socket.send(mensaje)
            return 
        
        filename = parts[1]
        offset = int(parts[2])
        size = int(parts[3])
        return get_slice(connection,filename, offset, size)
    
    elif command == "quit":
        
        if len(args) != 0:
            mensaje = f'{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}\r\n'
            mensaje = (mensaje.encode('utf-8'))
            connection.socket.send(mensaje)
            return
        return quit(connection)
    
    else:

        mensaje = f'{INVALID_COMMAND} {error_messages[INVALID_COMMAND]}\r\n'
        mensaje = (mensaje.encode('utf-8'))
        connection.socket.send(mensaje)
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

    print("Request: get_file_listing")
    connection.socket.send(mensaje.encode("ascii"))


def get_metadata(connection, FILENAME):
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
    except FileNotFoundError:
        print(f"The directory {connection.directory} does not exist.")
    except TypeError:
        print(f"The directory path is not a string: {connection.directory}")
    except PermissionError:
        print(f"Insufficient permissions to access the directory: {connection.directory}")

    # Verifica si el archivo solicitado existe
    for file in files:
        if file == FILENAME:
            # Obtiene el tamaño del archivo
            try:
                size = os.path.getsize(os.path.join(connection.directory, file))
            except:
                mensaje = f'{INTERNAL_ERROR} {error_messages[INTERNAL_ERROR]}\r\n'
                connection.socket.send(mensaje.encode("ascii"))
                return
            mensaje = f'{CODE_OK} {error_messages[CODE_OK]}\r\n'
            mensaje += f'{size}\r\n'

            # Codifica el mensaje en base64 y lo envía
            print("Request: get_metadata", FILENAME)
            connection.socket.send(mensaje.encode("ascii"))
            return
        
    # Si el archivo no existe envía un mensaje de error
    mensaje = f'{FILE_NOT_FOUND} {error_messages[FILE_NOT_FOUND]}\r\n'
    connection.socket.send(mensaje.encode("ascii"))


def get_slice(connection, FILENAME, OFFSET, SIZE):
    """
    Retorna un fragmento del archivo.
    """
    print("Request: get_slice", FILENAME, OFFSET, SIZE)
    # Verifica si el archivo solicitado existe
    if  not (os.path.isfile(os.path.join(connection.directory, FILENAME))):
        mensaje = f'{FILE_NOT_FOUND} {error_messages[FILE_NOT_FOUND]} \r\n'
        mensaje = mensaje.encode('utf-8')
        connection.socket.send(mensaje)
        return
     # verifica que no se saldra del archivo en la lectura
    elif os.path.getsize(os.path.join(connection.directory, FILENAME)) < OFFSET + SIZE:
        mensaje = f'{BAD_OFFSET} {error_messages[BAD_OFFSET]}\r\n'
        mensaje = mensaje.encode('utf-8')
        connection.socket.send(mensaje)
        return
    else:
    # Redacta la confirmación de lectura
        pathname = os.path.join(connection.directory, FILENAME)
        mensaje = f'{CODE_OK} {error_messages[CODE_OK]}\r\n'
        mensaje = mensaje.encode('utf-8')
        connection.socket.send(mensaje)
        
    #apertura y lectura del file
        with open(pathname, 'rb') as f:  # r = lectura, b = binario
            f.seek(OFFSET)

            mensaje = f.read(SIZE)              
    #codificación y envio de la lectura   
            mensaje = b64encode(mensaje)
            connection.socket.send(mensaje)
            mensaje = EOL.encode('utf-8')
            connection.socket.send(mensaje)
            return


def quit(connection):
    """
    Cierra la conexión.
    """
    connection.quit = True
    mensaje = f'{CODE_OK} {error_messages[CODE_OK]}\r\n'
    print("Request: quit")
    connection.socket.send(mensaje.encode("ascii"))
    return