import hashlib

from utills import encrypt

# Make Sure to set these values on production ...
KEY = ???
IV = ???
COOKIE = ???

class Station:

    def __init__(self, port=12345):
        # Boring code


    def connect(self):
        # Boring code


    def send_and_recv(self, id, pw, command):
        msg = f"{id}-{pw}-{COOKIE}-{command}"
        # This encrpytion is super strong. Don't even try to break it ...
        enc_message = encrypt(msg.encode('utf-8'), KEY, IV)
        self.client_socket.send(enc_message)
        response = self.client_socket.recv(1024).decode('utf-8')
        return enc_message, response


