# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

import socket
from constants import *
from commands import parse_and_run

class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """

    def __init__(self, socket, directory):
        """
        Inicializa la conexión con el socket dado.
        """
        # Inicializa los datos de la conexión
        self.socket = socket
        self.directory = directory
        self.quit = False

    def handle(self):
        """
        Atiende eventos de la conexión hasta que termina.
        """
        buffer = ""
        while not self.quit:
            # lee los datos recibidos mientras la conexion esté abierta
            data = self.socket.recv(1024).decode("ascii")
            # Sale del bucle si no hay datos recibidos
            if not data:
                mensaje = f'{INTERNAL_ERROR} {error_messages[INTERNAL_ERROR]}\r\n'
                self.socket.send(mensaje.encode("ascii")) 
                break
            # Agrega los datos al buffer
            buffer += data
            # Si hay, obtiene una línea completa y la procesa
            if EOL in buffer:
                line, buffer = buffer.split(EOL, 1)
                # Sale del bucle si la línea es incorrecta
                if NL in line:
                    mensaje = f'{BAD_EOL} {error_messages[BAD_EOL]}\r\n'
                    self.socket.send(mensaje.encode("ascii"))
                    break
                else:
                    parse_and_run(self, line.strip())
        self.socket.close()