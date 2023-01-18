import rsa


class Message:
    @staticmethod
    def send_encrypted_message(socket, public_key, message):
        socket.send(rsa.encrypt(message.encode(), public_key))

    @staticmethod
    def receive_and_decrypt(socket, private_key):
        cipher_text = socket.recv(1024)
        if cipher_text:
            print(cipher_text)
            try:
                decrypted_text = rsa.decrypt(cipher_text, private_key).decode()
                return decrypted_text
            except rsa.pkcs1.DecryptionError as e:
                print("Decryption failed:", e)
        return None
