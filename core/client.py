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
        self.target_client_public_key = None
        self.clients_list = []
        self.generate_rsa_key()
        self.is_chat_requester = False
        self.connection_message = ""
        self.chat_logger = chat_logger
        self.chat_connection_is_established = False
        self.handshake_is_made = False

    def connect_with_server(self):
        connection = self.server_socket.connect_ex((config.SERVER_PATH, config.SERVER_PORT))
        connection_established = connection == 0

        if connection_established:
            self.server_public_key = rsa.PublicKey.load_pkcs1(self.server_socket.recv(2048))
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
        if not pseudo_index.isnumeric() and pseudo_index >= len(self.clients_list):
            return None
        message = Message(config.CHOOSE_CLIENT_TYPE, self.clients_list[pseudo_index])
        Message.send_encrypted_message(self.server_socket, self.server_public_key, message)
        self.connection_message = Message.receive_and_decrypt(self.server_socket, self.private_key)
        if self.connection_message != 'ERROR':
            self.chat_socket.bind((config.CLIENT_PATH, config.CHAT_PORT))
            self.chat_socket.listen()
            accept_connections_thread = threading.Thread(target=self.listen_to_message_as_requester)
            accept_connections_thread.start()

    def wait_getting_chat_request(self):
        while True:
            if not self.chat_connection_is_established:
                self.chat_connection_is_established = self.chat_socket.connect_ex(
                    (config.CLIENT_PATH, config.CHAT_PORT)) == 0
            else:
                if not self.handshake_is_made:
                    self.target_client_public_key = rsa.PublicKey.load_pkcs1(self.chat_socket.recv(2048))
                    self.chat_socket.send(rsa.PublicKey.save_pkcs1(self.public_key))
                    self.handshake_is_made = True

    def listen_to_message_as_requester(self):
        while True:
            if self.is_chat_requester:
                (target, ip) = self.chat_socket.accept()
                if not self.target_client_socket:
                    self.target_client_socket = target
                    self.target_client_public_key = rsa.PublicKey.load_pkcs1(self.target_client_socket.recv(2048))
                    self.target_client_socket.send(rsa.PublicKey.save_pkcs1(self.public_key))
                message = Message.receive_and_decrypt(self.target_client_socket, self.private_key)
                if message:
                    self.chat_logger(message)

    def listen_to_message_as_receiver(self):
        while True:
            if not self.is_chat_requester and self.chat_connection_is_established:
                message = Message.receive_and_decrypt(self.target_client_socket, self.private_key)
                if message:
                    self.chat_logger(message)
