import json


class Message:
    def __init__(self, message_type, to, message):
        self.message_type = message_type
        self.to = to
        self.message = message

    @staticmethod
    def create_from_json(json_message: str) -> 'Message':
        message = json.loads(json_message)
        print(message)
        return Message(message["message_type"], message["to"],
                       message["message"])

    @staticmethod
    def get_from_socket(socket):
        json_received = socket.recv(1024).decode('utf-8')
        if json_received:
            return Message.create_from_json(json_received)
        return None

    def to_json(self):
        return json.dumps(self)
