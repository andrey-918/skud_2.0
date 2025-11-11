import tkinter as tk
from tkinter import ttk
from db.init_db import init_db
from gui.attendance_tab import AttendanceTab
from gui.settings_tab import SettingsTab

class AttendanceSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("СКУД")
        self.root.geometry("1200x800")

        # Initialize database
        init_db()

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Create tabs
        self.create_attendance_tab()
        self.create_settings_tab()

        # Select attendance tab by default
        self.notebook.select(0)

    def create_attendance_tab(self):
        """Tab for checking attendance (main functionality)"""
        frame = AttendanceTab(self.notebook)
        self.notebook.add(frame, text="Проверка посещаемости")

    def create_settings_tab(self):
        """Tab for settings (export reports, import meals)"""
        frame = SettingsTab(self.notebook)
        self.notebook.add(frame, text="Настройки")




def main():
    root = tk.Tk()
    app = AttendanceSystemGUI(root)
    root.mainloop()
