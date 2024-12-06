import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from typing import Dict, Any
from src.controllers.dynamic_controller import DynamicController
from src.services.dynamic_service import DynamicService
from src.repositories.dynamic_repository import DynamicRepository
from src.services.database_service import DatabaseService
from src.services.auth_service import AuthService
from src.ui.sidebar import Sidebar
from src.ui.navbar import Navbar
from src.ui.footer import Footer
from src.ui.dashboard import Dashboard
from src.utils.access_control import AccessControl
from src.config.app_config import AppConfig
from src.config.database_config import DatabaseConfig
import logging
import sys
import traceback


class EducaPlanApp(ttkb.Window):
    def __init__(self):
        super().__init__(themename="litera")
        self.title(AppConfig.APP_NAME)
        self.geometry("1024x768")
        self.center_window()
        
        self.setup_logging()
        
        print("Initializing EducaPlanApp")
        try:
            self.db_service = DatabaseService(DatabaseConfig.as_dict())
            self.auth_service = AuthService(self.db_service)
            self.current_user: Dict[str, Any] = {}

            self.setup_login_ui()
        except Exception as e:
            logging.exception("Failed to initialize application")
            self.show_error_message(f"Failed to initialize application: {str(e)}\n\n{traceback.format_exc()}")

    def setup_logging(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("educaplan.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )

    def center_window(self):
        self.update_idletasks()
        width = int(self.winfo_screenwidth() * 0.8)
        height = int(self.winfo_screenheight() * 0.8)
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def setup_login_ui(self):
        print("Setting up login UI")
        login_frame = ttk.Frame(self)
        login_frame.pack(fill=tk.BOTH, expand=True)

        center_frame = ttk.Frame(login_frame)
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ttk.Label(center_frame, text="Email:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.email_entry = ttk.Entry(center_frame)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(center_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(center_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        login_button = ttk.Button(center_frame, text="Login", command=self.login)
        login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.message_label = ttk.Label(center_frame, text="")
        self.message_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def login(self):
        print("Attempting login")
        email = self.email_entry.get()
        password = self.password_entry.get()
        user = self.auth_service.login(email, password)
        if user:
            print("Login successful")
            self.current_user = user
            self.initialize_main_components()
            self.setup_main_ui()
        else:
            print("Login failed")
            self.message_label.config(text="Login failed. Please try again.", style="Error.TLabel")

    def initialize_main_components(self):
        print("Initializing main components")
        repository = DynamicRepository(self.db_service)
        service = DynamicService(repository)
        self.dynamic_controller = DynamicController(service)

    def setup_main_ui(self):
        print("Setting up main UI")
        for widget in self.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.setup_ui_components(main_frame)

    def setup_ui_components(self, main_frame):
        print("Setting up UI components")
        navbar_config = AppConfig.get_navbar_config(
            username=self.current_user['Name'],
            logout_command=self.logout,
            exit_command=self.exit_app
        )
        footer_config = AppConfig.get_footer_config()

        self.navbar = Navbar(main_frame, navbar_config)
        self.navbar.pack(fill=tk.X, side=tk.TOP)

        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        allowed_categories = AccessControl.get_allowed_categories(self.current_user['Role_Name'])
        self.main_content = Dashboard(content_frame, self.current_user, self.dynamic_controller, allowed_categories)
        self.main_content.pack(fill=tk.BOTH, expand=True)

        self.footer = Footer(main_frame, footer_config)
        self.footer.pack(fill=tk.X, side=tk.BOTTOM)

    def logout(self):
        print("Logging out")
        self.auth_service.logout()
        self.current_user = {}
        
        # Destroy all existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        # Setup login UI
        self.setup_login_ui()

    def exit_app(self):
        print("Exiting application")
        self.quit()

    def show_error_message(self, message: str):
        print(f"Showing error message: {message}")
        error_window = ttkb.Toplevel(self)
        error_window.title("Error")
        error_window.geometry("400x200")
        
        ttk.Label(error_window, text=message, wraplength=380).pack(pady=20)
        ttk.Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)

    def handle_category_selection(self, event):
        category = event.widget.tk.call('set', 'event_data')
        print(f"Category selected: {category}")
        self.main_content.on_category_selected(category)

if __name__ == "__main__":
    app = EducaPlanApp()
    app.mainloop()

