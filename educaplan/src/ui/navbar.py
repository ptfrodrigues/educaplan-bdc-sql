import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb

class Navbar(ttk.Frame):
    def __init__(self, parent, config, **kwargs):
        super().__init__(parent, **kwargs)
        self.config = config
        self.setup_ui()

    def setup_ui(self):
        self.columnconfigure(1, weight=1)
        
        # Logo (text-based)
        logo_label = ttk.Label(self, text="EP", font=("Helvetica", 16, "bold"), foreground="#4a90e2", background="#ffffff", padding=5)
        logo_label.grid(row=0, column=0, padx=10, pady=5)

        # App name
        app_name_label = ttk.Label(self, text=self.config['app_name'], font=("Helvetica", 16, "bold"))
        app_name_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # User menu
        self.user_menu_button = ttk.Menubutton(self, text=self.config['username'])
        self.user_menu_button.grid(row=0, column=2, padx=10, pady=5, sticky="e")

        self.user_menu = tk.Menu(self.user_menu_button, tearoff=0)
        for item in self.config['menu_items']:
            self.user_menu.add_command(label=item['label'], command=item['command'])

        self.user_menu_button["menu"] = self.user_menu

