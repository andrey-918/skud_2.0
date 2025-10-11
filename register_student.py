import sqlite3
from db.init_db import init_db
from db.student import add_registration, finding_card

print("Регистрация существующего студента на приемы пищи:")
card_id = input("Введите ID карты студента: ")

student_id = finding_card(card_id)
if student_id is None:
    print("Студент с такой картой не найден")
    exit()

print("Выберите день недели (0=Понедельник, 1=Вторник, ..., 6=Воскресенье, или -1 для всех дней):")
day_choice = int(input("День недели (-1 для всех): "))
if day_choice == -1:
    # Register for all meals on all days
    conn = sqlite3.connect('skud.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, day_of_week FROM meals')
    all_meals = cursor.fetchall()
    conn.close()
    for meal_id, meal_name, day in all_meals:
        add_registration(student_id, meal_id)
        print(f"Зарегистрирован на {meal_name} в день {day}")
else:
    if not (0 <= day_choice <= 6):
        print("Неверный день недели")
        exit()
    conn = sqlite3.connect('skud.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM meals WHERE day_of_week = ?', (day_choice,))
    meals = cursor.fetchall()
    conn.close()
    if not meals:
        print("Нет приемов пищи для выбранного дня")
        exit()
    print("Приемы пищи для выбранного дня:")
    for meal_id, meal_name in meals:
        print(f"{meal_id}: {meal_name}")
    while True:
        meal_id = int(input("ID приема (0 для завершения): "))
        if meal_id == 0:
            break
        meal_ids = [m[0] for m in meals]
        if meal_id in meal_ids:
            add_registration(student_id, meal_id)
            meal_name = next(m[1] for m in meals if m[0] == meal_id)
            print(f"Зарегистрирован на {meal_name} в день {day_choice}")
        else:
            print("Неверный ID приема")
