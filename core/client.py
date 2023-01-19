import json
import socket
import threading
import time
import rsa
import core.consts as config
from core.message import Message


class Client:
    def __init__(self, chat_logger=print):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_public_key = None
        self.target_client_socket = None
        self.chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chat_socket_lock = threading.Lock()
        self.target_client_socket_lock = threading.Lock()
        self.target_client_public_key = None
        self.clients_list = []
        self.generate_rsa_key()
        self.is_chat_requester = False
        self.connection_message = ""
        self.chat_logger = chat_logger
        self.pseudo = ""
        self.chat_connection_is_established = False
        self.chat_connection_is_established_lock = threading.Lock()
        self.handshake_is_made = False
        self.handshake_is_made_lock = threading.Lock()
        self.listen_as_requester_thread = threading.Thread(target=self.listen_to_message_as_requester)
        self.listen_as_receiver_thread = threading.Thread(target=self.listen_to_message_as_receiver)
        self.listen_chat_connections_thread = threading.Thread(target=self.wait_getting_chat_request)
        self.ping_server_thread = threading.Thread(target=self.ping_server)
        self.close_listen_chat_connections_thread = None

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
        message = Message(config.REQUEST_ALL_TYPE, '')
        Message.send_encrypted_message(self.server_socket, self.server_public_key, message.to_json())
        server_message = Message.receive_and_decrypt(self.server_socket, self.private_key)
        if server_message:
            self.clients_list = json.loads(server_message)

    def choose_client(self, pseudo_index):
        print("inside choose client")
        if not len(pseudo_index) and not pseudo_index.isnumeric() and int(pseudo_index) >= len(self.clients_list):
            return None
        self.is_chat_requester = True
        message = Message(config.CHOOSE_CLIENT_TYPE, self.clients_list[int(pseudo_index)][0])
        Message.send_encrypted_message(self.server_socket, self.server_public_key, message.to_json())
        self.connection_message = Message.receive_and_decrypt(self.server_socket, self.private_key)
        if self.connection_message != 'NOT FOUND':
            self.chat_socket_lock.acquire()
            self.chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.chat_socket.bind((config.CLIENT_PATH, config.CHAT_PORT))
            self.chat_socket.listen()
            self.chat_socket_lock.release()
            self.listen_as_requester_thread.start()
        return self.connection_message

    def wait_getting_chat_request(self):
        connect_message = Message(config.CONNECT_CHAT_TYPE, '')
        Message.send_encrypted_message(self.server_socket, self.server_public_key, connect_message.to_json())
        while True:
            self.chat_connection_is_established_lock.acquire()
            self.chat_socket_lock.acquire()
            if not self.chat_connection_is_established and not self.is_chat_requester:
                print("Waiting for getting chat request")
                if self.chat_socket:
                    self.chat_connection_is_established = self.chat_socket.connect_ex(
                        (config.CLIENT_PATH, config.CHAT_PORT)) == 0
                else:
                    print("no chat socket")
                if self.chat_connection_is_established:
                    print("connected with the peer")
                    self.listen_as_receiver_thread.start()
            elif self.chat_socket:
                self.handshake_is_made_lock.acquire()
                if not self.handshake_is_made:
                    print("waiting for handshake")
                    self.target_client_socket_lock.acquire()
                    if self.is_chat_requester and self.target_client_socket:
                        key = self.target_client_socket.recv(2048)
                        if key:
                            self.target_client_public_key = rsa.PublicKey.load_pkcs1(key)
                            self.handshake_is_made = True
                            self.chat_logger("\nHANDSHAKE made\n\n")
                            print("handshake made")
                    elif not self.is_chat_requester and self.chat_socket:
                        key = self.chat_socket.recv(2048)
                        if key:
                            print("sending my public key as receiver")
                            self.chat_socket.send(rsa.PublicKey.save_pkcs1(self.public_key))
                            print("my public key as receiver is sent")
                            self.target_client_public_key = rsa.PublicKey.load_pkcs1(key)
                            self.handshake_is_made = True
                            self.chat_logger("HANDSHAKE made\n\n")
                            print("handshake made")
                    self.target_client_socket_lock.release()
                self.handshake_is_made_lock.release()
            self.chat_connection_is_established_lock.release()
            self.chat_socket_lock.release()

    def ping_server(self):
        ping = Message(config.PING_TYPE, self.pseudo)
        while True:
            Message.send_encrypted_message(self.server_socket, self.server_public_key, ping.to_json())
            time.sleep(10)

    def listen_to_message_as_requester(self):
        while True:
            self.target_client_socket_lock.acquire()
            if not self.target_client_socket:
                self.target_client_socket_lock.release()
                (target, ip) = self.chat_socket.accept()
                print("peer connected")
                self.target_client_socket_lock.acquire()
                self.target_client_socket = target
                print("sending my public key as requester")
                self.target_client_socket.send(rsa.PublicKey.save_pkcs1(self.public_key))
                print("public key as requester is sent")
                self.target_client_socket_lock.release()
            else:
                self.target_client_socket_lock.release()
                self.handshake_is_made_lock.acquire()
                if self.handshake_is_made:
                    print("waiting for chat")
                    message = Message.receive_and_decrypt(self.target_client_socket, self.private_key)
                    if message:
                        self.chat_logger(message + "\n")
                self.handshake_is_made_lock.release()

    def listen_to_message_as_receiver(self):
        message = Message.receive_and_decrypt(self.server_socket, self.private_key)
        if message:
            self.chat_logger(message + "\n")
        while True:
            self.handshake_is_made_lock.acquire()
            if self.handshake_is_made:
                print("waiting for chat")
                message = Message.receive_and_decrypt(self.chat_socket, self.private_key)
                if message:
                    self.chat_logger(message + "\n")
            self.handshake_is_made_lock.release()

    def exit_chat(self):
        disconnect_message = Message(config.DISCONNECT_CHAT_TYPE, '')
        Message.send_encrypted_message(self.server_socket, self.server_public_key, disconnect_message.to_json())
