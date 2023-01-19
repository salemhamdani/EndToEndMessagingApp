from PIL import Image, ImageTk
import tkinter as tk


class LoadingPage(tk.Toplevel):
    def __init__(self, text, context):
        super().__init__()
        self.context = context
        self.title("Loading")
        self.geometry("300x150+{}+{}".format(
            int((self.winfo_screenwidth() - 300) / 2),
            int((self.winfo_screenheight() - 150) / 2)
        ))
        self.loading_text = tk.Label(self, text=text)
        self.loading_text.pack()
        self.loading_spinner = tk.Label(self, width=100, height=100)
        self.loading_spinner.pack()
        self.gif = Image.open("ui/spinner.gif")
        self.frames = [ImageTk.PhotoImage(self.gif.copy())]
        self.gif.seek(1)
        self.update_spinner()

    def update_spinner(self):
        try:
            self.frames.append(ImageTk.PhotoImage(self.gif.copy()))
            self.gif.seek(self.gif.tell() + 1)
        except EOFError:
            self.gif.seek(0)
        self.loading_spinner["image"] = self.frames[-1]
        self.loading_spinner.after(100, self.update_spinner)

    def after_loading_page(self):
        connection = self.context.client.connect_with_server()
        self.destroy()
        if connection:
            self.context.deiconify()
            self.context.show_login_page()
        else:
            self.context.show_error_page()

    def show_bootstrap(self):
        self.context.withdraw()
        self.after(1000, self.after_loading_page)
        self.mainloop()

