import rsa
import json
import socket as s


class Message:
    def __init__(self, message_type, message):
        self.message_type = message_type
        self.message = message

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def send_encrypted_message(socket, public_key, message):
        socket.send(rsa.encrypt(message.encode(), public_key))

    @staticmethod
    def receive_and_decrypt(socket, private_key):
        try:
            cipher_text = socket.recv(2048)
            if cipher_text:
                try:
                    decrypted_text = rsa.decrypt(cipher_text, private_key).decode()
                    return decrypted_text
                except rsa.pkcs1.DecryptionError as e:
                    print("Decryption failed:", e)
            return None
        except s.timeout:
            return None
