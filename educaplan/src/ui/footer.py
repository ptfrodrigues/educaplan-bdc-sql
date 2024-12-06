import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb

class Footer(ttk.Frame):
    def __init__(self, parent, config, **kwargs):
        super().__init__(parent, **kwargs)
        self.config = config
        self.setup_ui()

    def setup_ui(self):
        self.message_label = ttk.Label(self, text="", font=self.config['font'])
        self.message_label.pack(pady=5)

    def show_message(self, message, message_type="info"):
        style = self.config['styles'].get(message_type, "TLabel")
        self.message_label.configure(style=style, text=message)
        self.after(self.config['message_duration'], self.clear_message)

    def clear_message(self):
        self.message_label.configure(text="")


