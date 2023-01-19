import json
import socket
import rsa
import threading
import core.consts as config
from core.message import Message
from services.auth import AuthService


class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
        self.socket.bind((config.SERVER_PATH, config.SERVER_PORT))
        self.generate_rsa_key()
        self.anonymous_clients = []
        self.authorized_clients = []

    def generate_rsa_key(self):
        (self.public_key, self.private_key) = rsa.newkeys(2048)

    def accept_connections(self):
        while True:
            client, ip = self.socket.accept()
            client.send(rsa.PublicKey.save_pkcs1(self.public_key))
            client_object = {'socket': client, 'public_key': rsa.PublicKey.load_pkcs1(client.recv(1024))}
            print("Anonymous client connected: ", ip)
            self.anonymous_clients.append(client_object)

    def accept_messages(self):
        while True:
            self.handle_anonymous_clients_messages()
            self.handle_authorized_clients_messages()

    def handle_authorized_clients_messages(self):
        for client in self.authorized_clients:
            msg = Message.receive_and_decrypt(client['socket'], self.private_key)
            if msg:
                print(msg)

    def handle_anonymous_clients_messages(self):
        for anonymous_client in self.anonymous_clients:
            msg = Message.receive_and_decrypt(anonymous_client['socket'], self.private_key)
            if msg:
                msg = json.loads(msg)
                if msg['message_type'] == config.REGISTER_TYPE:
                    if AuthService.handle_register(msg['message']):
                        print("Client registered")
                        Message.send_encrypted_message(anonymous_client['socket'], anonymous_client['public_key'],
                                                       "OK")
                    else:
                        print("Error registering client")
                        Message.send_encrypted_message(anonymous_client['socket'], anonymous_client['public_key'],
                                                       "Error")
                elif msg['message_type'] == config.LOGIN_TYPE:
                    if AuthService.handle_login(msg['message']):
                        print("Client logged in")
                        self.authorized_clients.append(anonymous_client)
                        self.anonymous_clients.remove(anonymous_client)
                        Message.send_encrypted_message(anonymous_client['socket'], anonymous_client['public_key'],
                                                       "OK")
                    else:
                        print("Error logging the client in")
                        Message.send_encrypted_message(anonymous_client['socket'], anonymous_client['public_key'],
                                                       "Error")

    def listen(self):
        self.socket.listen()
        print("listening on port", config.SERVER_PORT)
        accept_connections_thread = threading.Thread(target=self.accept_connections)
        accept_connections_thread.start()
        accept_messages_thread = threading.Thread(target=self.accept_messages)
        accept_messages_thread.start()


server = Server()
server.listen()
