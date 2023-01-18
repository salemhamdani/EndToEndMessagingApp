import random
import tkinter as tk
from core.client import Client
from core import conts as config
from ui.error_page import ErrorPage
from ui.loading_page import LoadingPage


def get_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.client = Client(config.SERVER_PATH, config.SERVER_PORT)
        self.bg_color = get_random_color()
        self.title("Client app")
        self.geometry("400x500+{}+{}".format(
            int((self.winfo_screenwidth() - 400) / 2),
            int((self.winfo_screenheight() - 500) / 2)
        ))
        self.configure(bg=self.bg_color)
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.chat_log = tk.Text(self, bg='white')
        self.message_frame = tk.Frame(self)
        self.message_text = tk.Entry(self.message_frame)

        self.bootstrap()

    def bootstrap(self):
        self.withdraw()
        loading_page = LoadingPage()
        loading_page.after(1000, lambda: self.after_loading_page(loading_page))
        loading_page.mainloop()

    def after_loading_page(self, loading_page):
        connection = self.client.connect_with_server()
        loading_page.destroy()
        if connection:
            self.deiconify()
            self.show_auth_page()
        else:
            self.show_error_page()

    def show_error_page(self):
        self.withdraw()
        error_page = ErrorPage("Error connecting to the server.", self)
        error_page.mainloop()

    def show_auth_page(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Username").pack()
        tk.Entry(self, textvariable=self.username).pack()
        tk.Label(self, text="Password").pack()
        tk.Entry(self, textvariable=self.password, show="*").pack()
        tk.Button(self, text="Login", command=self.login).pack()

    def show_menu_page(self):
        for widget in self.winfo_children():
            widget.destroy()
        title = tk.Label(self, text="Menu", font=("Helvetica", 18, "bold"), bg='white')
        title.pack(pady=20)
        menu_frame = tk.Frame(self, bg=self.bg_color)
        menu_frame.pack(pady=20)
        menu_frame.rowconfigure(0, weight=1)
        chat_button = tk.Button(menu_frame, text="Chat", font=("Helvetica", 14), width=10, height=2, bg='#3c3c3c',
                                fg='white', command=self.show_chat_page)
        chat_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)
        exit_button = tk.Button(menu_frame, text="Exit", font=("Helvetica", 14), width=10, height=2, bg='#3c3c3c',
                                fg='white', command=self.destroy)
        exit_button.grid(row=1, column=0, padx=10, pady=20, sticky=tk.N + tk.S + tk.E + tk.W)

    def show_chat_page(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.chat_log = tk.Text(self, bg=self.bg_color)
        self.chat_log.pack()
        message_frame = tk.Frame(self)
        message_frame.pack()
        self.message_text = tk.Entry(message_frame)
        self.message_text.pack(side=tk.LEFT)
        send_button = tk.Button(message_frame, text="Send", command=self.login)
        send_button.pack(side=tk.LEFT)

    def login(self):
        # ldap login logic
        return self.username


app = App()
app.mainloop()
