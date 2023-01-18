import socket
import rsa
import threading
from core.conts import SERVER_PORT, SERVER_PATH
from core.message import Message


class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((SERVER_PATH, SERVER_PORT))
        self.generate_rsa_key()
        self.anonymous_clients = []
        self.authorized_clients = []

    def generate_rsa_key(self):
        (self.public_key, self.private_key) = rsa.newkeys(512)

    def accept_connections(self):
        while True:
            client, ip = self.socket.accept()
            client.send(rsa.PublicKey.save_pkcs1(self.public_key))
            client_object = {'socket': client, 'public_key': rsa.PublicKey.load_pkcs1(client.recv(1024))}
            print("Anonymous client connected: ", ip)
            self.anonymous_clients.append(client_object)

    def accept_messages(self):
        print(self.anonymous_clients)
        while True:
            for anonymous_client in self.anonymous_clients:
                msg = Message.receive_and_decrypt(anonymous_client['socket'], self.private_key)
                if msg:
                    print("auth msg", msg)
                    if True:
                        print("authorized client")
                        self.authorized_clients.append(anonymous_client)
                        self.anonymous_clients.remove(anonymous_client)
                    else:
                        print("Failed to connect message")

            for client in self.authorized_clients:
                msg = Message.receive_and_decrypt(client['socket'], self.private_key)
                if msg:
                    print(msg)

    def listen(self):
        self.socket.listen()
        print("listening on port", SERVER_PORT)
        accept_connections_thread = threading.Thread(target=self.accept_connections)
        accept_connections_thread.start()
        accept_messages_thread = threading.Thread(target=self.accept_messages)
        accept_messages_thread.start()


server = Server()
server.listen()
