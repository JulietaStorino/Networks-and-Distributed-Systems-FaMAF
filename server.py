#!/usr/bin/env python
# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Revisión 2014 Carlos Bederián
# Revisión 2011 Nicolás Wolovick
# Copyright 2008-2010 Natalia Bidart y Daniel Moisset
# $Id: server.py 656 2013-03-18 23:49:11Z bc $

import optparse
import socket
import connection
from constants import *
import threading

def handle_thread(c, directory):
    """
    Atiende un hilo para conectarlo. Recibe un socket aceptado y un directorio.
    """
    # Crea una conexión con el socket dado
    c = connection.Connection(c, directory)
    # Atiende la conexión hasta que termine
    c.handle()

class Server(object):
    """
    El servidor, que crea y atiende el socket en la dirección y puerto
    especificados donde se reciben nuevas conexiones de clientes.
    """

    def __init__(self, addr=DEFAULT_ADDR, port=DEFAULT_PORT,
                 directory=DEFAULT_DIR):
        # Crea un socket para el servidor
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.socket.bind((addr, port))
        self.socket.listen(5)     
        # Inicializa los datos servidor
        self.address = addr
        self.port = port
        self.directory = directory
        print("Serving testdata on %s:%s" % (addr, port))

    def serve(self):
        """
        Loop principal del servidor. Se acepta una conexión a la vez
        y se espera a que concluya antes de seguir.
        """
        try:
            while True:
                # Acepta una conexión al server
                self.socket.listen()
                c, a = self.socket.accept()
                # Crea un hilo para atender la conexión
                lock = threading.Lock() 
                thread = threading.Thread(target=handle_thread, args=(c, self.directory))
                thread.start()
        except KeyboardInterrupt:
            print("Exiting...")

    def __del__(self):
        """
        Destructor de la clase, cierra el socket del servidor.
        """
        self.socket.close()


def main():
    """Parsea los argumentos y lanza el server"""

    parser = optparse.OptionParser()
    parser.add_option(
        "-p", "--port",
        help="Número de puerto TCP donde escuchar", default=DEFAULT_PORT)
    parser.add_option(
        "-a", "--address",
        help="Dirección donde escuchar", default=DEFAULT_ADDR)
    parser.add_option(
        "-d", "--datadir",
        help="Directorio compartido", default=DEFAULT_DIR)

    options, args = parser.parse_args()
    if len(args) > 0:
        parser.print_help()
        sys.exit(1)
    try:
        port = int(options.port)
    except ValueError:
        sys.stderr.write(
            "Numero de puerto invalido: %s\n" % repr(options.port))
        parser.print_help()
        sys.exit(1)

    server = Server(options.address, port, options.datadir)
    server.serve()


if __name__ == '__main__':
    main()
