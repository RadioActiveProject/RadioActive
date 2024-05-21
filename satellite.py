import ast
import hashlib
import socket

from riddles.transmit.utills import decrypt, encrypt

# Make Sure to set these values on production ...
KEY = ???
IV = ???
COOKIE = ???


class Satellite:

    def __init__(self, port):
        # Boring code

    def wait_for_connection(self):
        # Boring code

    def listen_and_move(self):
        while True:
            # Receive data from the client
            data = self.client_socket.recv(1024)

            try:
                dec_data = decrypt(data, KEY, IV)
                id, pw, cookie, command = dec_data.decode('latin-1').split("-")
                self.process_resquest(id, pw, cookie, command)

            except Exception as e:
                self.client_socket.send("BAD".encode('utf-8'))

    def process_resquest(self, id, pw, cookie, command):
        if cookie != COOKIE:
            self.client_socket.send("wrong cookie".encode('utf-8'))
            return

        if hashlib.sha256((id + cookie).encode('utf-8')).hexdigest() == pw and id == 'guest':
            self.client_socket.send("Logged in, but you dont have sufficient privileges".encode('utf-8'))
            return

        if hashlib.sha256((id + cookie).encode('utf-8')).hexdigest() == pw and id == 'admin':
            # success! command is executed using ProbeAPI
            return self.execute(command) 
            

        self.client_socket.send(f"invalid user".encode('utf-8'))
        return

