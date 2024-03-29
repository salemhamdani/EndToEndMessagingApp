import tkinter as tk
from core.client import Client
from core.consts import get_random_color
from ui.chat_page import ChatPage
from ui.error_page import ErrorPage
from ui.loading_page import LoadingPage
from ui.login_page import LoginPage
from ui.menu_page import MenuPage
from ui.register_page import RegisterPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.client = Client(self.log_chat_message)
        self.bg_color = get_random_color()
        self.title("Client app")
        self.geometry("500x650+{}+{}".format(
            int((self.winfo_screenwidth() - 400) / 2),
            int((self.winfo_screenheight() - 500) / 2)
        ))
        self.configure(bg=self.bg_color)
        self.loading_page = LoadingPage("Connecting to server", self)
        self.error_page = ErrorPage("Error connecting to the server.", self)
        self.login_page = LoginPage(self)
        self.register_page = RegisterPage(self)
        self.menu_page = MenuPage(self)
        self.chat_page = ChatPage(self)

        self.bootstrap()

    def bootstrap(self):
        self.loading_page.show_bootstrap()

    def show_error_page(self):
        self.error_page.show()

    def show_login_page(self):
        self.login_page.show()

    def show_register_page(self):
        self.register_page.show()

    def show_menu_page(self):
        self.menu_page.show()

    def show_chat_page(self):
        self.chat_page.show()

    def log_chat_message(self, *message):
        text = ' '.join(map(str, message))
        self.chat_page.chat_log.insert(tk.INSERT, text)


App().mainloop()
