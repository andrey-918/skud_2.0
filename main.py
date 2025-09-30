from db.student import check_student


card_id = int(input())

# check_student(card_id) == True if card_id % 6 == 0 else False

if check_student(card_id):
    print('Can eat')
else:
    print("Can't eat")