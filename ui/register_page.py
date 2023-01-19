import tkinter as tk
import json
from core.message import Message
import core.consts as config


class RegisterPage:
    def __init__(self, context):
        self.context = context
        self.pseudo = tk.StringVar()
        self.name = tk.StringVar()
        self.cart_id = tk.StringVar()
        self.password = tk.StringVar()
        self.alert_message = None

    def show(self):
        for widget in self.context.winfo_children():
            widget.destroy()
        title = tk.Label(self.context, text="Register", font=("Helvetica", 18, "bold"), bg=self.context.bg_color)
        title.pack(pady=20)
        self.alert_message = tk.Label(self.context, text="", font=("Helvetica", 15), bg=self.context.bg_color)
        self.alert_message.pack()

        register_frame = tk.Frame(self.context, bg=self.context.bg_color)
        register_frame.pack(pady=20)
        register_frame.rowconfigure(0, weight=1)
        cart_id_label = tk.Label(register_frame, text="Cart id", bg=self.context.bg_color)
        cart_id_label.grid(row=0, column=0, padx=10, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)
        cart_id_input = tk.Entry(register_frame, textvariable=self.cart_id)
        cart_id_input.grid(row=1, column=0, padx=10, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)
        name_label = tk.Label(register_frame, text="Full name", bg=self.context.bg_color)
        name_label.grid(row=2, column=0, padx=10, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)
        name_input = tk.Entry(register_frame, textvariable=self.name)
        name_input.grid(row=3, column=0, padx=10, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)
        pseudo_label = tk.Label(register_frame, text="Pseudo", bg=self.context.bg_color)
        pseudo_label.grid(row=4, column=0, padx=10, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)
        pseudo_input = tk.Entry(register_frame, textvariable=self.pseudo)
        pseudo_input.grid(row=5, column=0, padx=10, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)
        pwd_label = tk.Label(register_frame, text="Password", bg=self.context.bg_color)
        pwd_label.grid(row=6, column=0, padx=10, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)
        pwd_input = tk.Entry(register_frame, textvariable=self.password, show="*")
        pwd_input.grid(row=7, column=0, padx=10, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)
        register_button = tk.Button(register_frame, text="Register", command=self.register,
                                    font=("Helvetica", 14),
                                    bg='#3c3c3c',
                                    fg='white')
        register_button.grid(row=8, column=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)
        login_button = tk.Button(register_frame, text="Login", command=self.context.show_login_page,
                                 font=("Helvetica", 14),
                                 bg='#3c3c3c',
                                 fg='white')
        login_button.grid(row=9, column=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)
        exit_button = tk.Button(register_frame, text="Exit", font=("Helvetica", 14), width=10, height=2, bg='#3c3c3c',
                                fg='white', command=self.context.menu_page.exit)
        exit_button.grid(row=10, column=0, padx=10, pady=20, sticky=tk.N + tk.S + tk.E + tk.W)

    def register(self):
        register_object = {
            'name': self.name.get(),
            'cart_id': self.cart_id.get(),
            'pseudo': self.pseudo.get(),
            'password': self.password.get()
        }
        message = Message(config.REGISTER_TYPE, register_object)
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
            self.context.show_login_page()
            self.context.login_page.alert_message.configure(text="Account created, please log in", fg="green")
        else:
            self.alert_message.configure(text="Error", fg="red")
