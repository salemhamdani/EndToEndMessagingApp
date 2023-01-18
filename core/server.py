import socket

from message import Message
from services.auth import AuthService


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.anonymous_clients_sockets = []
        self.authorized_sockets = []

    def listen(self):
        self.socket.listen()
        print("listening on port", self.port)

        while True:
            client, ip = self.socket.accept()
            print("Anonymous client connected: ", ip)
            self.anonymous_clients_sockets.append(client)

            for anonymous_client in self.anonymous_clients_sockets:
                message = Message.get_from_socket(anonymous_client)
                if message:
                    if AuthService.handle_auth(message):
                        print("connected")
                    else:
                        print("Failed to connect message")

            for client in self.authorized_sockets:
                msg = Message.get_from_socket(client)
                if msg:
                    print(msg)


server = Server('localhost', 8000)
server.listen()
