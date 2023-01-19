import json
import socket
import threading

import rsa
import core.consts as config
from core.message import Message


class Client:
    def __init__(self, chat_logger=print):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
        self.server_public_key = None
        self.target_client_socket = None
        self.chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.target_server_public_key = None
        self.clients_list = []
        self.generate_rsa_key()
        self.is_chat_requester = False
        self.connection_message = ""
        self.chat_logger = chat_logger

    def connect_with_server(self):
        connection = self.server_socket.connect_ex((config.SERVER_PATH, config.SERVER_PORT))
        connection_established = connection == 0

        if connection_established:
            self.server_public_key = rsa.PublicKey.load_pkcs1(self.server_socket.recv(1024))
            self.server_socket.send(rsa.PublicKey.save_pkcs1(self.public_key))
        return connection_established

    def generate_rsa_key(self):
        (self.public_key, self.private_key) = rsa.newkeys(2048)

    def request_clients_list(self):
        self.is_chat_requester = True
        message = Message(config.REQUEST_ALL_TYPE, '')
        Message.send_encrypted_message(self.server_socket, self.server_public_key, message.to_json())
        server_message = Message.receive_and_decrypt(self.server_socket, self.private_key)
        if server_message:
            self.clients_list = json.loads(server_message)

    def choose_client(self, pseudo_index):
        if pseudo_index >= len(self.clients_list):
            return None
        message = Message(config.CHOOSE_CLIENT_TYPE, self.clients_list[pseudo_index])
        Message.send_encrypted_message(self.server_socket, self.server_public_key, message)
        self.connection_message = Message.receive_and_decrypt(self.server_socket, self.private_key)
        if self.connection_message != 'ERROR':
            self.chat_socket.bind((config.CLIENT_PATH, config.CHAT_PORT))
            self.chat_socket.listen()
            accept_connections_thread = threading.Thread(target=self.listen_to_message)
            accept_connections_thread.start()

    def listen_to_message(self):
        return None

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
