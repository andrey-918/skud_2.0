import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db.meals import get_current_meal, get_meal_name
from db.student import finding_card, check_student, log_attendance

class AttendanceTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_ui()
        self.update_current_meal()

    def create_ui(self):
        # Current meal info
        info_frame = ttk.LabelFrame(self, text="Текущий прием пищи")
        info_frame.pack(fill=tk.X, padx=10, pady=10)

        self.current_meal_label = ttk.Label(info_frame, text="Определение текущего приема пищи...")
        self.current_meal_label.pack(padx=10, pady=10)

        ttk.Button(info_frame, text="Обновить", command=self.update_current_meal).pack(pady=5)

        # Attendance check
        check_frame = ttk.LabelFrame(self, text="Проверка доступа")
        check_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(check_frame, text="ID карты студента:", font=('Arial', 12)).pack(pady=10)

        self.attendance_card_id = ttk.Entry(check_frame, font=('Arial', 14))
        self.attendance_card_id.pack(pady=5, ipady=5)

        ttk.Button(check_frame, text="Проверить доступ", command=self.check_attendance).pack(pady=20)

        self.attendance_result = ttk.Label(check_frame, text="", font=('Arial', 16, 'bold'))
        self.attendance_result.pack(pady=20)

    def update_current_meal(self):
        """Update current meal information"""
        current_meal = get_current_meal()
        if current_meal is None:
            self.current_meal_label.config(text="Сейчас нет времени приема пищи")
            self.current_meal_id = None
        else:
            meal_name = get_meal_name(current_meal)
            day_names = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
            day_name = day_names[datetime.now().weekday()]
            self.current_meal_label.config(text=f"Текущий прием: {meal_name} ({day_name})")
            self.current_meal_id = current_meal

    def check_attendance(self):
        """Check student attendance for current meal"""
        if self.current_meal_id is None:
            self.attendance_result.config(text="Сейчас нет времени приема пищи", foreground="red")
            return

        card_id_str = self.attendance_card_id.get()
        if not card_id_str:
            self.attendance_result.config(text="Введите ID карты", foreground="red")
            return

        try:
            card_id = card_id_str
            status = check_student(card_id, self.current_meal_id)
            if status == 'registered':
                student_id = finding_card(card_id)
                log_attendance(student_id, self.current_meal_id, 'came')
                self.attendance_result.config(text="ДОСТУП РАЗРЕШЕН", foreground="green")
            elif status == 'not_registered':
                student_id = finding_card(card_id)
                log_attendance(student_id, self.current_meal_id, 'came_without_registration')
                self.attendance_result.config(text="ДОСТУП РАЗРЕШЕН (БЕЗ ЗАПИСИ)", foreground="orange")
            else:  # unknown_card
                self.attendance_result.config(text="ДОСТУП ЗАПРЕЩЕН", foreground="red")
        except Exception as e:
            self.attendance_result.config(text=f"Ошибка: {str(e)}", foreground="red")

        # Clear the input
        self.attendance_card_id.delete(0, tk.END)
