import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import sqlite3
from datetime import datetime
import openpyxl
from db.init_db import init_db
from db.student import (
    finding_card, check_student, log_attendance, add_student,
    add_registration, get_all_students, update_student, delete_student
)
from db.meals import get_current_meal, get_meal_name
from db.reports import get_attendance_report, get_all_attendance_records

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
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Управление студентами")

        # Left panel - Student list
        left_frame = ttk.Frame(frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(left_frame, text="Список студентов:", font=('Arial', 12, 'bold')).pack(pady=5)

        # Treeview for students
        columns = ('ID', 'Имя', 'Карта')
        self.student_tree = ttk.Treeview(left_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.student_tree.heading(col, text=col)
            self.student_tree.column(col, width=100)
        self.student_tree.pack(fill=tk.BOTH, expand=True)

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.student_tree.yview)
        self.student_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(btn_frame, text="Обновить список", command=self.load_students).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Добавить студента", command=self.add_student_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Импорт из XLSX", command=self.import_students_from_xlsx).pack(side=tk.LEFT, padx=5)

        # Right panel - Actions
        right_frame = ttk.Frame(frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(right_frame, text="Действия:", font=('Arial', 12, 'bold')).pack(pady=5)

        action_frame = ttk.LabelFrame(right_frame, text="Выберите действие")
        action_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Button(action_frame, text="Изменить студента", command=self.edit_student_dialog).pack(fill=tk.X, pady=5)
        ttk.Button(action_frame, text="Удалить студента", command=self.delete_student).pack(fill=tk.X, pady=5)

        # Load initial data
        self.load_students()

    def create_registration_tab(self):
        """Tab for registering students for meals"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Регистрация на приемы пищи")

        # Student selection
        student_frame = ttk.LabelFrame(frame, text="Выбор студента")
        student_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(student_frame, text="ID карты студента:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.reg_card_id = ttk.Entry(student_frame)
        self.reg_card_id.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Button(student_frame, text="Найти студента", command=self.find_student_for_registration).grid(row=0, column=2, padx=5, pady=5)

        self.student_info_label = ttk.Label(student_frame, text="")
        self.student_info_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)

        # Day selection
        day_frame = ttk.LabelFrame(frame, text="Выбор дня")
        day_frame.pack(fill=tk.X, padx=10, pady=10)

        self.day_var = tk.StringVar(value="-1")
        days = [("-1", "Все дни"), ("0", "Понедельник"), ("1", "Вторник"), ("2", "Среда"),
                ("3", "Четверг"), ("4", "Пятница"), ("5", "Суббота"), ("6", "Воскресенье")]

        for i, (val, text) in enumerate(days):
            ttk.Radiobutton(day_frame, text=text, variable=self.day_var, value=val).grid(row=i//4, column=i%4, padx=5, pady=5, sticky=tk.W)

        # Meals selection
        meals_frame = ttk.LabelFrame(frame, text="Выбор приемов пищи")
        meals_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.meals_listbox = tk.Listbox(meals_frame, selectmode=tk.MULTIPLE, height=10)
        self.meals_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(meals_frame, orient=tk.VERTICAL, command=self.meals_listbox.yview)
        self.meals_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(btn_frame, text="Загрузить приемы пищи", command=self.load_meals_for_registration).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Зарегистрировать", command=self.register_student).pack(side=tk.LEFT, padx=5)

    def create_reports_tab(self):
        """Tab for viewing attendance reports"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Отчеты")

        # Report type selection
        type_frame = ttk.LabelFrame(frame, text="Тип отчета")
        type_frame.pack(fill=tk.X, padx=10, pady=10)

        self.report_type = tk.StringVar(value="specific")
        ttk.Radiobutton(type_frame, text="Отчет по конкретному приему пищи", variable=self.report_type,
                       value="specific", command=self.toggle_report_type).pack(anchor=tk.W, padx=5, pady=5)
        ttk.Radiobutton(type_frame, text="Общая таблица посещаемости", variable=self.report_type,
                       value="all", command=self.toggle_report_type).pack(anchor=tk.W, padx=5, pady=5)

        # Specific meal report controls
        self.specific_frame = ttk.LabelFrame(frame, text="Параметры отчета")
        self.specific_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(self.specific_frame, text="День недели:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.report_day = ttk.Combobox(self.specific_frame, values=[
            "0 - Понедельник", "1 - Вторник", "2 - Среда", "3 - Четверг",
            "4 - Пятница", "5 - Суббота", "6 - Воскресенье"])
        self.report_day.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        self.report_day.current(0)

        ttk.Button(self.specific_frame, text="Показать приемы пищи", command=self.load_meals_for_report).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(self.specific_frame, text="Прием пищи:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.report_meal = ttk.Combobox(self.specific_frame)
        self.report_meal.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Button(self.specific_frame, text="Сгенерировать отчет", command=self.generate_specific_report).grid(row=1, column=2, padx=5, pady=5)

        # Report display area
        display_frame = ttk.LabelFrame(frame, text="Результат")
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.report_text = tk.Text(display_frame, wrap=tk.WORD, height=20)
        self.report_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # General report button (initially hidden)
        self.all_report_btn = ttk.Button(frame, text="Показать общую таблицу", command=self.generate_all_report)
        # Initially hide the all report button
        self.all_report_btn.pack_forget()

    def create_attendance_tab(self):
        """Tab for checking attendance (main functionality)"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Проверка посещаемости")

        # Current meal info
        info_frame = ttk.LabelFrame(frame, text="Текущий прием пищи")
        info_frame.pack(fill=tk.X, padx=10, pady=10)

        self.current_meal_label = ttk.Label(info_frame, text="Определение текущего приема пищи...")
        self.current_meal_label.pack(padx=10, pady=10)

        ttk.Button(info_frame, text="Обновить", command=self.update_current_meal).pack(pady=5)

        # Attendance check
        check_frame = ttk.LabelFrame(frame, text="Проверка доступа")
        check_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(check_frame, text="ID карты студента:", font=('Arial', 12)).pack(pady=10)

        self.attendance_card_id = ttk.Entry(check_frame, font=('Arial', 14))
        self.attendance_card_id.pack(pady=5, ipady=5)

        ttk.Button(check_frame, text="Проверить доступ", command=self.check_attendance).pack(pady=20)

        self.attendance_result = ttk.Label(check_frame, text="", font=('Arial', 16, 'bold'))
        self.attendance_result.pack(pady=20)

        # Initialize current meal
        self.update_current_meal()

    # Student management methods
    def load_students(self):
        """Load all students into the treeview"""
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)

        students = get_all_students()
        for student in students:
            self.student_tree.insert('', tk.END, values=student)

    def add_student_dialog(self):
        """Dialog to add a new student"""
        name = simpledialog.askstring("Добавить студента", "Имя студента:")
        if not name:
            return

        card_id_str = simpledialog.askstring("Добавить студента", "ID карты:")
        if not card_id_str:
            return

        try:
            card_id = int(card_id_str)
            add_student(name, card_id)
            messagebox.showinfo("Успех", f"Студент {name} добавлен с картой {card_id}")
            self.load_students()
        except ValueError:
            messagebox.showerror("Ошибка", "ID карты должен быть числом")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить студента: {str(e)}")

    def edit_student_dialog(self):
        """Dialog to edit selected student"""
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите студента для редактирования")
            return

        item = self.student_tree.item(selected[0])
        student_id, current_name, current_card = item['values']

        name = simpledialog.askstring("Изменить студента", "Новое имя:", initialvalue=current_name)
        card_id_str = simpledialog.askstring("Изменить студента", "Новый ID карты:", initialvalue=str(current_card))

        try:
            card_id = int(card_id_str) if card_id_str else None
            update_student(student_id, name, card_id)
            messagebox.showinfo("Успех", "Информация о студенте обновлена")
            self.load_students()
        except ValueError:
            messagebox.showerror("Ошибка", "ID карты должен быть числом")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить студента: {str(e)}")

    def delete_student(self):
        """Delete selected student"""
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите студента для удаления")
            return

        if not messagebox.askyesno("Подтверждение", "Удалить студента и все связанные записи?"):
            return

        item = self.student_tree.item(selected[0])
        student_id = item['values'][0]

        try:
            delete_student(student_id)
            messagebox.showinfo("Успех", "Студент удален")
            self.load_students()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить студента: {str(e)}")

    def import_students_from_xlsx(self):
        """Import students from XLSX file"""
        filename = filedialog.askopenfilename(title="Выберите XLSX файл", filetypes=[("Excel files", "*.xlsx")])
        if not filename:
            return

        try:
            wb = openpyxl.load_workbook(filename)
            ws = wb.active

            # Get next card_id
            conn = sqlite3.connect('skud.db')
            cursor = conn.cursor()
            cursor.execute('SELECT MAX(card_id) FROM students')
            max_card = cursor.fetchone()[0]
            next_card = (max_card + 1) if max_card else 1
            conn.close()

            added = 0
            registered = 0
            for row in range(9, ws.max_row + 1):
                name = ws.cell(row=row, column=3).value
                if name and isinstance(name, str) and name.strip():
                    try:
                        add_student(name.strip(), next_card)
                        student_id = finding_card(next_card)
                        next_card += 1
                        added += 1

                        # Import registrations
                        for d in range(6):  # Monday to Saturday
                            for m in range(3):  # Breakfast, Lunch, Dinner
                                col = 4 + d * 3 + m
                                if ws.cell(row=row, column=col).value == 1:
                                    meal_id = d * 3 + m + 1
                                    add_registration(student_id, meal_id)
                                    registered += 1
                    except sqlite3.IntegrityError:
                        # Skip if card_id conflict
                        pass

            messagebox.showinfo("Успех", f"Добавлено {added} студентов и {registered} регистраций")
            self.load_students()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось импортировать: {str(e)}")

    # Registration methods
    def find_student_for_registration(self):
        """Find student by card ID for registration"""
        card_id_str = self.reg_card_id.get()
        if not card_id_str:
            messagebox.showwarning("Предупреждение", "Введите ID карты")
            return

        try:
            card_id = int(card_id_str)
            student_id = finding_card(card_id)
            if student_id:
                # Get student name
                conn = sqlite3.connect('skud.db')
                cursor = conn.cursor()
                cursor.execute('SELECT name FROM students WHERE id = ?', (student_id,))
                name = cursor.fetchone()[0]
                conn.close()
                self.student_info_label.config(text=f"Найден студент: {name} (ID: {student_id})")
                self.current_reg_student_id = student_id
            else:
                self.student_info_label.config(text="Студент не найден")
                self.current_reg_student_id = None
        except ValueError:
            messagebox.showerror("Ошибка", "ID карты должен быть числом")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска: {str(e)}")

    def load_meals_for_registration(self):
        """Load meals based on selected day"""
        day_choice = self.day_var.get()

        self.meals_listbox.delete(0, tk.END)

        conn = sqlite3.connect('skud.db')
        cursor = conn.cursor()

        if day_choice == "-1":
            cursor.execute('SELECT id, name, day_of_week FROM meals ORDER BY day_of_week, id')
        else:
            cursor.execute('SELECT id, name, day_of_week FROM meals WHERE day_of_week = ? ORDER BY id', (int(day_choice),))

        meals = cursor.fetchall()
        conn.close()

        day_names = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

        for meal_id, name, day in meals:
            day_name = day_names[day] if day_choice == "-1" else ""
            display_text = f"{meal_id}: {name} {day_name}".strip()
            self.meals_listbox.insert(tk.END, display_text)
            # Store meal_id for later use
            if not hasattr(self, 'meal_ids'):
                self.meal_ids = []
            self.meal_ids.append(meal_id)

    def register_student(self):
        """Register student for selected meals"""
        if not hasattr(self, 'current_reg_student_id') or self.current_reg_student_id is None:
            messagebox.showwarning("Предупреждение", "Сначала найдите студента")
            return

        selected_indices = self.meals_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Предупреждение", "Выберите приемы пищи")
            return

        try:
            registered_count = 0
            for idx in selected_indices:
                if hasattr(self, 'meal_ids') and idx < len(self.meal_ids):
                    meal_id = self.meal_ids[idx]
                    add_registration(self.current_reg_student_id, meal_id)
                    registered_count += 1

            messagebox.showinfo("Успех", f"Студент зарегистрирован на {registered_count} приемов пищи")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось зарегистрировать: {str(e)}")

    # Reports methods
    def toggle_report_type(self):
        """Toggle between specific meal report and all reports"""
        if self.report_type.get() == "specific":
            self.all_report_btn.pack_forget()
            self.specific_frame.pack(fill=tk.X, padx=10, pady=10, after=self.report_text)
        else:
            self.specific_frame.pack_forget()
            self.all_report_btn.pack(fill=tk.X, padx=10, pady=10, after=self.report_text)

    def load_meals_for_report(self):
        """Load meals for selected day in reports"""
        day_str = self.report_day.get()
        if not day_str:
            return

        day_of_week = int(day_str.split()[0])

        conn = sqlite3.connect('skud.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM meals WHERE day_of_week = ?', (day_of_week,))
        meals = cursor.fetchall()
        conn.close()

        self.report_meal['values'] = [f"{meal[0]}: {meal[1]}" for meal in meals]
        if meals:
            self.report_meal.current(0)

    def generate_specific_report(self):
        """Generate report for specific meal"""
        meal_str = self.report_meal.get()
        day_str = self.report_day.get()

        if not meal_str or not day_str:
            messagebox.showwarning("Предупреждение", "Выберите день и прием пищи")
            return

        try:
            meal_id = int(meal_str.split(':')[0])
            day_of_week = int(day_str.split()[0])

            report = get_attendance_report(meal_id, day_of_week)
            meal_name = get_meal_name(meal_id)

            day_names = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(tk.END, f"Отчет для {meal_name} в {day_names[day_of_week]}\n\n")

            self.report_text.insert(tk.END, "Пришли:\n")
            for name in report['came']:
                self.report_text.insert(tk.END, f" - {name}\n")

            self.report_text.insert(tk.END, "\nНе пришли:\n")
            for name in report['didnt_come']:
                self.report_text.insert(tk.END, f" - {name}\n")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сгенерировать отчет: {str(e)}")

    def generate_all_report(self):
        """Generate comprehensive attendance report"""
        try:
            records = get_all_attendance_records()
            if not records:
                self.report_text.delete(1.0, tk.END)
                self.report_text.insert(tk.END, "Нет данных о посещаемости.")
                return

            # Group by day_of_week
            from collections import defaultdict
            days_data = defaultdict(lambda: defaultdict(dict))

            for record in records:
                day = record['day_of_week']
                student = record['student_name']
                meal = record['meal_name']
                status = record['status']
                days_data[day][student][meal] = status

            day_names = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

            self.report_text.delete(1.0, tk.END)

            for day in sorted(days_data.keys()):
                self.report_text.insert(tk.END, f"\nДень: {day_names[day]}\n")
                students = sorted(days_data[day].keys())
                meals = sorted(set(m for s in days_data[day].values() for m in s.keys()))

                # Fix meal order: Breakfast, Lunch, Dinner
                meal_order = ['Breakfast', 'Lunch', 'Dinner']
                meals = [meal for meal in meal_order if meal in meals]

                # Header
                header = f"{'Студент':<20}" + "".join(f"{meal:<15}" for meal in meals)
                self.report_text.insert(tk.END, header + "\n")
                self.report_text.insert(tk.END, "-" * len(header) + "\n")

                # Rows
                for student in students:
                    row = f"{student:<20}"
                    for meal in meals:
                        status = days_data[day][student].get(meal, 'not_registered')
                        status_ru = {
                            'came': 'пришел',
                            'didnt_come': 'не пришел',
                            'not_registered': 'не записан'
                        }.get(status, status)
                        row += f"{status_ru:<15}"
                    self.report_text.insert(tk.END, row + "\n")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сгенерировать отчет: {str(e)}")

    # Attendance methods
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
            card_id = int(card_id_str)
            if check_student(card_id, self.current_meal_id):
                student_id = finding_card(card_id)
                log_attendance(student_id, self.current_meal_id, 'came')
                self.attendance_result.config(text="ДОСТУП РАЗРЕШЕН", foreground="green")
            else:
                self.attendance_result.config(text="ДОСТУП ЗАПРЕЩЕН", foreground="red")
        except ValueError:
            self.attendance_result.config(text="ID карты должен быть числом", foreground="red")
        except Exception as e:
            self.attendance_result.config(text=f"Ошибка: {str(e)}", foreground="red")

        # Clear the input
        self.attendance_card_id.delete(0, tk.END)


def main():
    root = tk.Tk()
    app = AttendanceSystemGUI(root)
    root.mainloop()


