import threading
import tkinter as tk

from core.message import Message


class ChatPage:
    def __init__(self, context):
        self.context = context
        self.message_frame = tk.Frame(self.context)
        self.chat_log = tk.Text(self.context, bg=self.context.bg_color)
        self.message_text = tk.Entry(self.message_frame)
        self.connected = False

    def show(self):
        for widget in self.context.winfo_children():
            widget.destroy()
        self.message_frame = tk.Frame(self.context)
        self.chat_log = tk.Text(self.context, bg=self.context.bg_color)
        self.message_text = tk.Entry(self.message_frame)
        self.chat_log.pack()
        self.message_frame.pack()
        self.message_text.pack(side=tk.LEFT)
        send_button = tk.Button(self.message_frame, text="Send", command=self.send)
        send_button.pack(side=tk.LEFT)
        exit_button = tk.Button(self.context, text="EXIT", command=self.exit)
        exit_button.pack()
        self.chat_log.insert(tk.INSERT, "TYPE /all to see all available clients\n\n")
        self.context.client.listen_chat_connections_thread.start()

    def insert_clients_list(self):
        self.chat_log.insert(tk.INSERT, "Available clients: \n\n")
        for index, pseudo in enumerate(self.context.client.clients_list):
            if pseudo[0] == self.context.client.pseudo:
                pass
            else:
                self.chat_log.insert(tk.INSERT, f"{index}- {pseudo[0]}\n")
        if len(self.context.client.clients_list) > 1:
            self.chat_log.insert(tk.INSERT, "\nEnter the number of the client you want to connect to\n\n")
        else:
            self.chat_log.insert(tk.INSERT, "No connected client found\n")

    def send(self):
        if self.message_text.get() == "/all":
            self.context.client.request_clients_list()
            self.insert_clients_list()
            self.message_text.delete(0, tk.END)
            return
        if not self.context.client.handshake_is_made:
            print("not inside all request")
            if self.message_text.get().isnumeric():
                result = self.context.client.choose_client(self.message_text.get())
                if not result:
                    self.insert_clients_list()
                self.chat_log.insert(tk.INSERT, result)
            self.message_text.delete(0, tk.END)
            return
        else:
            print("Sending message")
            message = f"\n{self.context.client.pseudo} > {self.message_text.get()}"
            public_key = self.context.client.target_client_public_key
            self.chat_log.insert(tk.INSERT, message + "\n")
            if self.context.client.is_chat_requester:
                sock = self.context.client.target_client_socket
            else:
                sock = self.context.client.chat_socket
            Message.send_encrypted_message(sock, public_key, message)
            self.message_text.delete(0, tk.END)
            return

    def exit(self):
        self.context.client.exit_chat()
        self.context.show_menu_page()
        self.context.client.close_listen_chat_connections_thread = 1
