import socket


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_with_server(self):
        connection = self.server_socket.connect_ex((self.host, self.port))
        return connection == 0

    def sendMessage(self, message):
        self.server_socket.send(message.encode('utf-8'))
