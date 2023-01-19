import rsa


class RSAHelper:

    @staticmethod
    def load_public_key(path):
        try:
            with open(path, 'rb') as f:
                pub_key = rsa.PublicKey.load_pkcs1(f.read())
            return pub_key
        except:
            print("Public key not found.")

    @staticmethod
    def load_private_key(path):
        try:
            with open(path, 'rb') as f:
                private_key = rsa.PrivateKey.load_pkcs1(f.read())
            return private_key
        except:
            return False

    @staticmethod
    def generate_keys(public_path='keys/rsa_public-key.pem', private_path='keys/rsa_private-key.pem'):
        (pub_key, private_key) = rsa.newkeys(4096)
        with open(public_path, 'wb') as f:
            f.write(pub_key.save_pkcs1('PEM'))

        with open(private_path, 'wb') as f:
            f.write(private_key.save_pkcs1('PEM'))
        print("Keys generated.")

    @staticmethod
    def encrypt(msg, key):
        return rsa.encrypt(msg.encode('ascii'), key)

    @staticmethod
    def decrypt(ciphertext, key):
        try:
            return rsa.decrypt(ciphertext, key).decode('ascii')
        except:
            return False

    @staticmethod
    def sign_sha256(msg, key):
        return rsa.sign(msg.encode('ascii'), key, 'SHA-256')

    @staticmethod
    def verify_sha256(msg: str, signature, key):
        try:
            return rsa.verify(msg.encode('ascii'), signature, key) == 'SHA-256'
        except:
            return False
