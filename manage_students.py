from db.init_db import init_db
from db.student import get_all_students, update_student, delete_student

# init_db()  # Commented out to preserve data

def display_students():
    students = get_all_students()
    print("Список студентов:")
    for student in students:
        print(f"ID: {student[0]}, Имя: {student[1]}, Карта: {student[2]}")

display_students()

action = input("\nВыберите действие: 1 - Изменить, 2 - Удалить, 0 - Выход: ")
if action == '1':
    student_id = int(input("Введите ID студента: "))
    name = input("Новое имя (оставьте пустым, если не менять): ")
    card_id_str = input("Новый ID карты (оставьте пустым, если не менять): ")
    card_id = int(card_id_str) if card_id_str else None
    update_student(student_id, name if name else None, card_id)
    print("Информация обновлена.")
elif action == '2':
    student_id = int(input("Введите ID студента для удаления: "))
    delete_student(student_id)
    print("Студент удален.")
else:
    print("Выход.")

display_students()
