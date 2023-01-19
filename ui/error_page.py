import tkinter as tk


class ErrorPage(tk.Toplevel):
    def __init__(self, message, context):
        super().__init__()
        self.context = context
        self.title("Error")
        self.geometry("300x150+{}+{}".format(
            int((self.winfo_screenwidth() - 300) / 2),
            int((self.winfo_screenheight() - 150) / 2)
        ))

        self.message = tk.Label(self, text=message, font=("Helvetica", 14))
        self.message.pack(pady=20)

        self.ok_button = tk.Button(self, text="OK", command=self.close)
        self.ok_button.pack(pady=10)

    def close(self):
        self.destroy()
        self.context.destroy()

    def show(self):
        self.context.withdraw()
        self.mainloop()
