from db.init_db import init_db
from db.student import check_student, finding_card, log_attendance
from db.meals import get_current_meal, get_meal_name

# init_db()  # Commented out to preserve registrations

current_meal = get_current_meal()
if current_meal is None:
    print("No meal time now")
else:
    meal_name = get_meal_name(current_meal)
    print(f"Current meal: {meal_name}")

    card_id = int(input("Enter card ID: "))

    if check_student(card_id, current_meal):
        student_id = finding_card(card_id)
        log_attendance(student_id, current_meal, 'came')
        print('Can eat')
    else:
        print("Can't eat")
