import json
import socket
import rsa
import threading
import core.consts as config
from core.message import Message
from services.auth import AuthService
from services.user_repository import UserRepository


class Server:
    def __init__(self, logger=print):
        self.logger = logger
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
        self.socket.bind((config.SERVER_PATH, config.SERVER_PORT))
        self.generate_rsa_key()
        self.anonymous_clients = []
        self.authorized_clients = []
        self.clients_in_chat = []
        self.anonymous_clients_lock = threading.Lock()
        self.authorized_clients_lock = threading.Lock()
        self.clients_in_chat_lock = threading.Lock()
        self.listen()

    def generate_rsa_key(self):
        (self.public_key, self.private_key) = rsa.newkeys(2048)

    def accept_connections(self):
        while True:
            client, ip = self.socket.accept()
            client.send(rsa.PublicKey.save_pkcs1(self.public_key))
            client.settimeout(1)
            client_object = {'socket': client, 'public_key': rsa.PublicKey.load_pkcs1(client.recv(2048))}
            self.logger("Anonymous client connected: ", ip)
            self.anonymous_clients_lock.acquire()
            self.anonymous_clients.append(client_object)
            self.anonymous_clients_lock.release()

    def accept_messages(self):
        while True:
            self.handle_anonymous_clients_messages()
            self.handle_authorized_clients_messages()

    def handle_authorized_clients_messages(self):
        authorized_client_exited = None
        for client in self.authorized_clients:
            msg = Message.receive_and_decrypt(client['socket'], self.private_key)
            if msg == b'':
                self.logger(f"client {client['pseudo']} exited the app")
                authorized_client_exited = client
            if msg:
                msg = json.loads(msg)
                if msg['message_type'] == config.REQUEST_ALL_TYPE:
                    self.logger(f"{client['pseudo']} requested to see all connected users")
                    clients = UserRepository.get_connected_users()
                    self.logger(f"connected users are {clients}")
                    Message.send_encrypted_message(client['socket'], client['public_key'], json.dumps(clients))
                if msg['message_type'] == config.CHOOSE_CLIENT_TYPE:
                    found = False
                    for target_client in self.authorized_clients:
                        target_client_pseudo = target_client['pseudo'].decode('utf')
                        if target_client_pseudo == msg['message']:
                            found = True
                            Message.send_encrypted_message(target_client['socket'], target_client['public_key'],
                                                           f"Peer to peer connection established with {client['pseudo'].decode('utf')}\n")
                            Message.send_encrypted_message(client['socket'], client['public_key'],
                                                           f"Peer to peer connection established with {target_client_pseudo}\n")
                            self.logger(f"Peer to peer connection is established between {client['pseudo'].decode('utf')} and {target_client_pseudo}")
                        else:
                            pass
                    if not found:
                        Message.send_encrypted_message(client['socket'], client['public_key'], 'NOT FOUND')
                if msg['message_type'] == config.CONNECT_CHAT_TYPE:
                    self.logger(f"{client['pseudo']} connected to his chat page")
                    AuthService.connect_chat(client)
                if msg['message_type'] == config.DISCONNECT_CHAT_TYPE:
                    self.logger(f"{client['pseudo']} disconnected from his chat page")
                    AuthService.disconnect_chat(client)
        if authorized_client_exited:
            self.authorized_clients.remove(authorized_client_exited)

    def handle_anonymous_clients_messages(self):
        self.anonymous_clients_lock.acquire()
        logged_in = None
        anonymous_client_exited = None
        for anonymous_client in self.anonymous_clients:
            msg = Message.receive_and_decrypt(anonymous_client['socket'], self.private_key)
            if msg == b'':
                self.logger("anonymous client exited the app")
                anonymous_client_exited = anonymous_client
            if msg:
                msg = json.loads(msg)
                if msg['message_type'] == config.REGISTER_TYPE:
                    if AuthService.handle_register(msg['message']):
                        self.logger(f"Client {msg['message']['pseudo']} registered")
                        Message.send_encrypted_message(anonymous_client['socket'], anonymous_client['public_key'],
                                                       "OK")
                    else:
                        self.logger("Error registering client")
                        Message.send_encrypted_message(anonymous_client['socket'], anonymous_client['public_key'],
                                                       "Error")
                elif msg['message_type'] == config.LOGIN_TYPE:
                    if AuthService.handle_login(msg['message']):
                        self.logger(f"Client {msg['message']['pseudo'].encode()} logged in")
                        self.authorized_clients.append(
                            {**anonymous_client, 'pseudo': msg['message']['pseudo'].encode('utf-8')})
                        logged_in = anonymous_client
                        Message.send_encrypted_message(anonymous_client['socket'], anonymous_client['public_key'],
                                                       "OK")
                    else:
                        self.logger("Error logging the client in")
                        Message.send_encrypted_message(anonymous_client['socket'], anonymous_client['public_key'],
                                                       "Error")
        if logged_in:
            self.anonymous_clients.remove(logged_in)
        if anonymous_client_exited:
            self.anonymous_clients.remove(anonymous_client_exited)
        self.anonymous_clients_lock.release()

    def listen(self):
        self.socket.listen()
        self.logger("listening on port", config.SERVER_PORT)
        threading.Thread(target=self.accept_connections).start()
        threading.Thread(target=self.accept_messages).start()
