from PIL import Image, ImageTk
import tkinter as tk


class LoadingPage(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Loading")
        self.geometry("300x150+{}+{}".format(
            int((self.winfo_screenwidth() - 300) / 2),
            int((self.winfo_screenheight() - 150) / 2)
        ))
        self.loading_text = tk.Label(self, text="Connecting to the server...")
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
