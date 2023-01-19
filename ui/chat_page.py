import tkinter as tk


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

        self.chat_log.pack()
        self.message_frame.pack()
        self.message_text.pack(side=tk.LEFT)
        send_button = tk.Button(self.message_frame, text="Send", command=self.send)
        send_button.pack(side=tk.LEFT)

    def insert_clients_list(self):
        self.chat_log.insert("Available clients: ")
        for index, pseudo in enumerate(self.context.client.clients_list):
            self.chat_log.insert(tk.INSERT, f"{index}- {pseudo}")
        self.chat_log.insert("Enter the number of the client you want to connect to")

    def send(self):
        if not self.connected:
            result = self.context.client.choose_client(self.message_text)
            if result:
                self.connected = True
            else:
                self.insert_clients_list()
                self.message_text.delete(0, tk.END)
        else:
            return None
