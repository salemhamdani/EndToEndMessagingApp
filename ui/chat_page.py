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
        self.chat_log.insert(tk.INSERT, "TYPE /all to see all available clients\n")
        # accept_connections_thread = threading.Thread(target=self.context.client.wait_getting_chat_request())
        # accept_connections_thread.start()

    def insert_clients_list(self):
        self.chat_log.insert(tk.INSERT, "Available clients: \n")
        for index, pseudo in enumerate(self.context.client.clients_list):
            self.chat_log.insert(tk.INSERT, f"{index}- {pseudo}\n")
        if len(self.context.client.clients_list):
            self.chat_log.insert(tk.INSERT, "Enter the number of the client you want to connect to\n")
        else:
            self.chat_log.insert(tk.INSERT, "No connected client found\n")

    def send(self):
        if not self.context.client.chat_connection_is_established:
            if self.message_text.get() == "/all":
                self.insert_clients_list()
            else:
                result = self.context.client.choose_client(self.message_text.get())
                if not result:
                    self.insert_clients_list()
        else:
            if self.context.client.is_chat_requester:
                Message.send_encrypted_message(
                    self.context.client.target_client_socket,
                    self.context.client.target_client_public_key,
                    self.message_text.get()
                )
            else:
                Message.send_encrypted_message(
                    self.context.client.chat_socket,
                    self.context.client.target_client_public_key,
                    self.message_text.get()
                )

        self.message_text.delete(0, tk.END)
