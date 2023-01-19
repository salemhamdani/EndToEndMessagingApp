import tkinter as tk


class ChatPage:
    def __init__(self, context):
        self.context = context
        self.message_frame = tk.Frame(self.context)
        self.chat_log = tk.Text(self.context, bg=self.context.bg_color)
        self.message_text = tk.Entry(self.message_frame)
        self.password = tk.StringVar()

    def show(self):
        for widget in self.context.winfo_children():
            widget.destroy()

        self.chat_log.pack()
        self.message_frame.pack()
        self.message_text.pack(side=tk.LEFT)
        send_button = tk.Button(self.message_frame, text="Send", command=self.send)
        send_button.pack(side=tk.LEFT)

    def send(self):
        return None
