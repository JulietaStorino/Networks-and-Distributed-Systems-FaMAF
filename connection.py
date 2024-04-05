# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

import socket
from constants import *
from base64 import b64encode
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
                break                
            # Agrega los datos al buffer
            buffer += data
            # Verifica si el buffer contiene una línea completa
            if "\r\n" in buffer:
                # Obtiene la línea completa
                line, buffer = buffer.split("\r\n", 1)
                if "\n" in line or "\r" in line:
                    self.socket.send(f'{BAD_EOL} BAD_EOL\r\n' .encode('ascii'))
                    self.close()
                    # Procesa la línea recibida
                else:
                    parse_and_run(self, line)
