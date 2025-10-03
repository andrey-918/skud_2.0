import sqlite3
from db.reports import get_attendance_report, get_all_attendance_records
from db.meals import get_meal_name

def show_attendance_for_meal():

    print("Просмотр отчетов о посещаемости:")
    print("Выберите день недели (0=Понедельник, 1=Вторник, ..., 6=Воскресенье):")
    day_of_week = int(input("День недели: "))
    if not (0 <= day_of_week <= 6):
        print("Неверный день недели")
        return

    conn = sqlite3.connect('skud.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM meals WHERE day_of_week = ?', (day_of_week,))
    meals = cursor.fetchall()
    conn.close()

    if not meals:
        print("Нет приемов пищи для выбранного дня")
        return

    print("Приемы пищи для выбранного дня:")
    for meal_id, meal_name in meals:
        print(f"{meal_id}: {meal_name}")

    meal_id = int(input("Выберите ID приема для отчета: "))
    meal_ids = [m[0] for m in meals]
    if meal_id in meal_ids:
        report = get_attendance_report(meal_id, day_of_week)
        meal_name = get_meal_name(meal_id)
        print(f"\nОтчет для {meal_name} в день {day_of_week}:")
        print("Пришли:")
        for name in report['came']:
            print(f" - {name}")
        print("Не пришли:")
        for name in report['didnt_come']:
            print(f" - {name}")
    else:
        print("Неверный ID приема")

def show_all_attendance():
    records = get_all_attendance_records()
    if not records:
        print("Нет данных о посещаемости.")
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

    for day in sorted(days_data.keys()):
        print(f"\nДень: {day_names[day]}")
        students = sorted(days_data[day].keys())
        meals = sorted(set(m for s in days_data[day].values() for m in s.keys()))

        # Fix meal order: Breakfast, Lunch, Dinner
        meal_order = ['Breakfast', 'Lunch', 'Dinner']
        meals = [meal for meal in meal_order if meal in meals]

        # Header
        header = f"{'Студент':<20}" + "".join(f"{meal:<15}" for meal in meals)
        print(header)
        print("-" * len(header))

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
            print(row)

def main():
    print("Выберите действие:")
    print("1 - Просмотр отчета по приему пищи")
    print("2 - Просмотр таблицы со всеми записями на все приемы пищи")
    choice = input("Введите номер действия: ")
    if choice == '1':
        show_attendance_for_meal()
    elif choice == '2':
        show_all_attendance()
    else:
        print("Неверный выбор")

if __name__ == '__main__':
    main()
