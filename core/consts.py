import os
import random

APP_NAME = "EndToEndMessagingApp"
SERVER_PATH = 'localhost'
CLIENT_PATH = 'localhost'
SERVER_PORT = 8080
CHAT_PORT = 3030
REGISTER_TYPE = 'REGISTER'
LOGIN_TYPE = 'LOGIN'
CHAT_TYPE = 'CHAT'
REQUEST_ALL_TYPE = 'REQUEST_ALL'
CHOOSE_CLIENT_TYPE = 'CHOOSE_CLIENT'


def get_app_path():
    abs_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(abs_path)
    dirs = dir_path.split(os.path.sep)
    while dirs[-1] != APP_NAME:
        dirs.pop()
    app_name_dir = os.path.sep.join(dirs)
    return app_name_dir


def get_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


SERVER_KEY_PATH = get_app_path() + 'server/pair_key.key'
SERVER_CERTIFICATE_PATH = get_app_path() + 'server/certificate.crt'
CLIENTS_CERTIFICATES_DIRECTORY = 'clients/certificates/'
