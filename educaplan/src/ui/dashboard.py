import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttkb
from typing import Dict, Any, List
from src.controllers.dynamic_controller import DynamicController
from src.models.dynamic_entity import DynamicEntity
from src.utils.access_control import AccessControl
from src.ui.sidebar import Sidebar
import logging

class Dashboard(ttk.Frame):
    def __init__(self, parent: Any, user: Dict[str, Any], dynamic_controller: DynamicController, allowed_categories: List[str], **kwargs):
        super().__init__(parent, **kwargs)
        self.user = user
        self.dynamic_controller = dynamic_controller
        self.allowed_categories = allowed_categories
        self.current_category = None
        self.view_to_table_map = self.create_view_to_table_map()
        self.setup_ui()

    def create_view_to_table_map(self):
        view_to_table = {
            'Users_View': 'Users',
            'Roles_View': 'Roles',
            'Courses_View': 'Courses',
            'Modules_View': 'Modules',
            'Topics_View': 'Topics',
            'Materials_View': 'Materials',
            'Students_View': 'Students',
            'Attendance_View': 'Attendance',
            'Feedback_View': 'Feedback',
            'Progress_View': 'Progress',
            'Grades_View': 'Grades',
            'My_Courses_View': 'Courses',
        }
        return view_to_table

    def setup_ui(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.sidebar = Sidebar(self, self.user['Role_Name'], self.allowed_categories, self.on_category_selected)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        content_frame = ttk.Frame(self)
        content_frame.grid(row=0, column=1, sticky="nsew")
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(1, weight=1)

        self.breadcrumb = ttk.Label(content_frame, text="", font=("Helvetica", 12))
        self.breadcrumb.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.notebook = ttk.Notebook(content_frame)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

    def on_category_selected(self, category):
        print(f"Category selected: {category}")
        self.current_category = category
        self.update_breadcrumb()
        self.load_category_tables(category)

    def update_breadcrumb(self):
        self.breadcrumb.config(text=f"Home > {self.current_category}")

    def load_category_tables(self, category):
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)

        tables = AccessControl.get_tables_in_category(category)
        for table in tables:
            self.create_table_tab(table)

    def create_table_tab(self, view_name: str):
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=view_name.replace('_View', '').capitalize())

        columns = self.dynamic_controller.get_table_columns(view_name)
        tree = ttk.Treeview(tab_frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=100)

        tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.refresh_table(tree, view_name)

        if self.user['Role_Name'] in ["Teacher", "Administrator"]:
            btn_frame = ttk.Frame(tab_frame)
            btn_frame.pack(pady=10)

            table_name = self.view_to_table_map.get(view_name, view_name)
            ttk.Button(btn_frame, text=f"Add {table_name}", command=lambda: self.add_item(view_name, table_name)).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text=f"Edit {table_name}", command=lambda: self.edit_item(view_name, table_name, tree)).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text=f"Delete {table_name}", command=lambda: self.delete_item(view_name, table_name, tree)).pack(side=tk.LEFT, padx=5)

    def refresh_table(self, tree: ttk.Treeview, view_name: str):
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            items = self.dynamic_controller.get_all(view_name)
            if not items:
                logging.warning(f"No data found for view {view_name}")
                messagebox.showinfo("No Data", f"No data found in {view_name}")
            for item in items:
                tree.insert("", "end", values=tuple(item.to_dict().values()))
        except Exception as e:
            logging.error(f"Error refreshing view {view_name}: {e}")
            messagebox.showerror("Error", f"Failed to load data for {view_name}")

    def add_item(self, view_name: str, table_name: str):
        columns = self.dynamic_controller.get_table_columns(table_name)
        window_height = min(len(columns) * 60 + 100, 600)  # 60 pixels per field, plus 100 for padding and buttons
        window_width = 400

        add_window = ttkb.Toplevel(self)
        add_window.title(f"Add {table_name}")
        add_window.geometry(f"{window_width}x{window_height}")
        add_window.resizable(False, False)

        # Center the window
        screen_width = add_window.winfo_screenwidth()
        screen_height = add_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        add_window.geometry(f"+{x}+{y}")

        # Create a canvas to center the content
        canvas = tk.Canvas(add_window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a frame inside the canvas
        frame = ttk.Frame(canvas)
        canvas.create_window((window_width // 2, window_height // 2), window=frame, anchor="center")

        entries = {}
        for col in columns:
            if col != 'id':
                ttk.Label(frame, text=f"{col.capitalize()}:").pack(pady=5)
                entries[col] = ttk.Entry(frame)
                entries[col].pack(pady=5)

        def save_item():
            data = {col: entry.get().strip() for col, entry in entries.items()}
            if all(data.values()):
                try:
                    self.dynamic_controller.create(table_name, data)
                    tree = self.notebook.winfo_children()[self.allowed_categories.index(self.current_category)].winfo_children()[0]
                    self.refresh_table(tree, view_name)
                    add_window.destroy()
                except Exception as e:
                    logging.error(f"Error creating new item in {table_name}: {e}")
                    messagebox.showerror("Error", f"Failed to create new item in {table_name}: {str(e)}")
            else:
                messagebox.showerror("Error", "Please fill in all fields")

        ttk.Button(frame, text="Save", command=save_item).pack(pady=10)

        # Update the canvas scroll region
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def edit_item(self, view_name: str, table_name: str, tree: ttk.Treeview):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", f"Please select a {table_name} to edit")
            return

        item_id = tree.item(selected[0])['values'][0]
        try:
            item = self.dynamic_controller.get_by_id(table_name, item_id)
            if not item:
                messagebox.showerror("Error", f"Failed to retrieve {table_name} with id {item_id}")
                return

            window_height = min(len(item.to_dict()) * 60 + 100, 600)  # 60 pixels per field, plus 100 for padding and buttons
            window_width = 400

            edit_window = ttkb.Toplevel(self)
            edit_window.title(f"Edit {table_name}")
            edit_window.geometry(f"{window_width}x{window_height}")
            edit_window.resizable(False, False)

            # Center the window
            screen_width = edit_window.winfo_screenwidth()
            screen_height = edit_window.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            edit_window.geometry(f"+{x}+{y}")

            # Create a canvas to center the content
            canvas = tk.Canvas(edit_window)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Add a frame inside the canvas
            frame = ttk.Frame(canvas)
            canvas.create_window((window_width // 2, window_height // 2), window=frame, anchor="center")

            entries = {}
            for col, value in item.to_dict().items():
                if col != 'id':
                    ttk.Label(frame, text=f"{col.capitalize()}:").pack(pady=5)
                    entries[col] = ttk.Entry(frame)
                    entries[col].insert(0, value)
                    entries[col].pack(pady=5)

            def update_item():
                data = {col: entry.get() for col, entry in entries.items() if entry.get()}
                if all(data.values()):
                    try:
                        self.dynamic_controller.update(table_name, item_id, data)
                        self.refresh_table(tree, view_name)
                        edit_window.destroy()
                    except Exception as e:
                        logging.error(f"Error updating item in {table_name}: {e}")
                        messagebox.showerror("Error", f"Failed to update item in {table_name}: {str(e)}")
                else:
                    messagebox.showerror("Error", "Please fill in all fields")

            ttk.Button(frame, text="Update", command=update_item).pack(pady=10)

            frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
        except Exception as e:
            logging.error(f"Error editing item in {table_name}: {e}")
            messagebox.showerror("Error", f"Failed to edit item in {table_name}: {str(e)}")

    def delete_item(self, view_name: str, table_name: str, tree: ttk.Treeview):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", f"Please select a {table_name} to delete")
            return

        item_id = tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this {table_name}?"):
            try:
                self.dynamic_controller.delete(table_name, item_id)
                self.refresh_table(tree, view_name)
            except Exception as e:
                logging.error(f"Error deleting item from {table_name}: {e}")
                messagebox.showerror("Error", f"Failed to delete item from {table_name}: {str(e)}")

