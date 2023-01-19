import tkinter as tk


class MenuPage:
    def __init__(self, context):
        self.context = context

    def show(self):
        for widget in self.context.winfo_children():
            widget.destroy()
        title = tk.Label(self.context, text="Menu", font=("Helvetica", 18, "bold"), bg='white')
        title.pack(pady=20)
        menu_frame = tk.Frame(self.context, bg=self.context.bg_color)
        menu_frame.pack(pady=20)
        menu_frame.rowconfigure(0, weight=1)
        chat_button = tk.Button(menu_frame, text="Chat", font=("Helvetica", 14), width=10, height=2, bg='#3c3c3c',
                                fg='white', command=self.context.show_chat_page)
        chat_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)
        exit_button = tk.Button(menu_frame, text="Exit", font=("Helvetica", 14), width=10, height=2, bg='#3c3c3c',
                                fg='white', command=self.context.destroy)
        exit_button.grid(row=1, column=0, padx=10, pady=20, sticky=tk.N + tk.S + tk.E + tk.W)
