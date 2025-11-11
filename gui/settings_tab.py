import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import openpyxl
import sqlite3
from datetime import datetime
from collections import defaultdict
from db.reports import get_all_attendance_records
from gui.student_tab import StudentTab
from gui.registration_tab import RegistrationTab
from gui.reports_tab import ReportsTab

class SettingsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_ui()

    def create_ui(self):
        # Management buttons
        management_frame = ttk.LabelFrame(self, text="Управление")
        management_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(management_frame, text="Управление студентами", command=self.open_student_management).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(management_frame, text="Регистрация на приемы пищи", command=self.open_registration_management).pack(side=tk.LEFT, padx=5, pady=5)

        # Import/Export buttons
        io_frame = ttk.LabelFrame(self, text="Импорт/Экспорт")
        io_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(io_frame, text="Экспорт посещаемости в Excel", command=self.open_export_management).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(io_frame, text="Импорт приемов пищи из Excel", command=RegistrationTab(self).import_students_from_xlsx).pack(side=tk.LEFT, padx=5, pady=5)


    def open_student_management(self):
        """Open student management in a new window"""
        top = tk.Toplevel(self)
        top.title("Управление студентами")
        top.geometry("1000x600")
        StudentTab(top).pack(fill=tk.BOTH, expand=True)

    def open_export_management(self):
        """Open export management in a new window"""
        top = tk.Toplevel(self)
        top.title("Экспорт приемов пищи")
        top.geometry("1000x600")
        ReportsTab(top).pack(fill=tk.BOTH, expand=True)

    def open_registration_management(self):
        """Open registration management in a new window"""
        top = tk.Toplevel(self)
        top.title("Регистрация на приемы пищи")
        top.geometry("1000x600")
        RegistrationTab(top).pack(fill=tk.BOTH, expand=True)

    def open_reports_management(self):
        """Open reports management in a new window"""
        top = tk.Toplevel(self)
        top.title("Отчеты")
        top.geometry("1000x600")
        ReportsTab(top).pack(fill=tk.BOTH, expand=True)