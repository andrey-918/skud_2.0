def finding_card(card_id):
    return card_id if card_id % 3 == 0 else None

def student_sheet(student_id):
    return student_id if student_id % 2 == 0 else None

def check_student(card_id):
    student_id = finding_card(card_id)

    if student_id == None or student_sheet(student_id) == None:
        return False
    return True