import tkinter as tk
from tkinter import ttk
from db.init_db import init_db
from gui.student_tab import StudentTab
from gui.registration_tab import RegistrationTab
from gui.reports_tab import ReportsTab
from gui.attendance_tab import AttendanceTab

class AttendanceSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("СКУД")
        self.root.geometry("1000x700")

        # Initialize database
        init_db()

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Create tabs
        self.create_student_tab()
        self.create_registration_tab()
        self.create_reports_tab()
        self.create_attendance_tab()

    def create_student_tab(self):
        """Tab for managing students (add, edit, delete, view)"""
        frame = StudentTab(self.notebook)
        self.notebook.add(frame, text="Управление студентами")

    def create_registration_tab(self):
        """Tab for registering students for meals"""
        frame = RegistrationTab(self.notebook)
        self.notebook.add(frame, text="Регистрация на приемы пищи")

    def create_reports_tab(self):
        """Tab for exporting attendance reports to Excel"""
        frame = ReportsTab(self.notebook)
        self.notebook.add(frame, text="Отчеты")

    def create_attendance_tab(self):
        """Tab for checking attendance (main functionality)"""
        frame = AttendanceTab(self.notebook)
        self.notebook.add(frame, text="Проверка посещаемости")




def main():
    root = tk.Tk()
    app = AttendanceSystemGUI(root)
    root.mainloop()
