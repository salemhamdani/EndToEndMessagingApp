import socket
import rsa
from core.consts import SERVER_PATH, SERVER_PORT
from core.message import Message


class Client:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
        self.server_public_key = None
        self.target_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.target_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
        self.target_server_public_key = None
        self.generate_rsa_key()

    def connect_with_server(self):
        connection = self.server_socket.connect_ex((SERVER_PATH, SERVER_PORT))
        connection_established = connection == 0

        if connection_established:
            self.server_public_key = rsa.PublicKey.load_pkcs1(self.server_socket.recv(1024))
            self.server_socket.send(rsa.PublicKey.save_pkcs1(self.public_key))
        return connection_established

    def generate_rsa_key(self):
        (self.public_key, self.private_key) = rsa.newkeys(2048)

    def connect_to_client(self):
        message = "GET_CLIENTS"
        message = message.encode('utf8')
        self.server_socket.send(rsa.encrypt(message, self.server_public_key))
        clients = self.server_socket.recv(1024).decode('ascii')
        print("Available clients: " + clients)
        target_client = input("Enter the nickname of the client you want to connect to: ")
        message = f"CONNECT_TO {target_client}"
        message = message.encode('utf8')
        self.server_socket.send(rsa.encrypt(message, self.server_public_key))
        target_address = self.server_socket.recv(1024).decode('ascii')
        target_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_client_socket.connect((target_address.split(':')[0], int(target_address.split(':')[1])))
        target_client_socket.send(f"Connected to {self.nickname}".encode('ascii'))
        print("Connected to " + target_client)
