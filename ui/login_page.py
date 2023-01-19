import tkinter as tk
import core.consts as config
from core.message import Message


class LoginPage:
    def __init__(self, context):
        self.context = context
        self.pseudo = tk.StringVar()
        self.password = tk.StringVar()
        self.alert_message = None

    def show(self):
        for widget in self.context.winfo_children():
            widget.destroy()
        title = tk.Label(self.context, text="Log in", font=("Helvetica", 18, "bold"), bg=self.context.bg_color)
        title.pack(pady=20)
        self.alert_message = tk.Label(self.context, text="", font=("Helvetica", 15), bg=self.context.bg_color)
        self.alert_message.pack()
        auth_frame = tk.Frame(self.context, bg=self.context.bg_color)
        auth_frame.pack(pady=20)
        auth_frame.rowconfigure(0, weight=1)
        pseudo_label = tk.Label(auth_frame, text="Pseudo", bg=self.context.bg_color)
        pseudo_label.grid(row=0, column=0, padx=10, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)
        pseudo_input = tk.Entry(auth_frame, textvariable=self.pseudo)
        pseudo_input.grid(row=1, column=0, padx=10, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)
        pwd_label = tk.Label(auth_frame, text="Password", bg=self.context.bg_color)
        pwd_label.grid(row=2, column=0, padx=10, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)
        pwd_input = tk.Entry(auth_frame, textvariable=self.password, show="*")
        pwd_input.grid(row=3, column=0, padx=10, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)
        login_button = tk.Button(auth_frame, text="Login", command=self.login, font=("Helvetica", 14),
                                 bg='#3c3c3c',
                                 fg='white')
        login_button.grid(row=4, column=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)
        register_button = tk.Button(auth_frame, text="Register", command=self.context.show_register_page,
                                    font=("Helvetica", 14),
                                    bg='#3c3c3c',
                                    fg='white')
        register_button.grid(row=5, column=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

    def login(self):
        login_object = {
            'pseudo': self.pseudo.get(),
            'password': self.password.get()
        }
        message = Message(config.LOGIN_TYPE, login_object)
        Message.send_encrypted_message(
            self.context.client.server_socket,
            self.context.client.server_public_key,
            message.to_json()
        )
        server_message = Message.receive_and_decrypt(
            self.context.client.server_socket,
            self.context.client.private_key
        )
        if server_message and server_message == 'OK':
            self.context.show_menu_page()
        else:
            self.alert_message.configure(text="Error", fg="red")
