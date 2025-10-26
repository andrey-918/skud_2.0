import sqlite3

def get_attendance_report(meal_id, day_of_week):
    conn = sqlite3.connect('skud.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT r.student_id, s.name, COALESCE(a.status, 'didnt_come') as status
        FROM registrations r
        LEFT JOIN students s ON r.student_id = s.id
        LEFT JOIN attendance a ON r.student_id = a.student_id AND r.meal_id = a.meal_id AND (strftime('%w', a.timestamp) + 6) % 7 = ?
        WHERE r.meal_id = ? AND s.id IS NOT NULL
    ''', (day_of_week, meal_id))

    rows = cursor.fetchall()
    conn.close()

    report = {
        'came': [],
        'didnt_come': [],
        'came_without_registration': []
    }

    for student_id, name, status in rows:
        if status == 'came':
            report['came'].append(name)
        elif status == 'came_without_registration':
            report['came_without_registration'].append(name)
        else:
            report['didnt_come'].append(name)

    return report

def get_all_attendance_records():
    conn = sqlite3.connect('skud.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT DISTINCT s.name as student_name, m.id as meal_id, m.day_of_week, m.name as meal_name,
        CASE WHEN r.id IS NOT NULL THEN COALESCE(a.status, 'didnt_come') ELSE 'not_registered' END as status
        FROM students s
        CROSS JOIN meals m
        LEFT JOIN registrations r ON r.student_id = s.id AND r.meal_id = m.id
        LEFT JOIN attendance a ON a.student_id = s.id AND a.meal_id = m.id
        ORDER BY s.name, m.day_of_week, m.id
    ''')

    rows = cursor.fetchall()
    conn.close()

    records = []
    for student_name, meal_id, day_of_week, meal_name, status in rows:
        # Override status if came_without_registration exists
        if status == 'not_registered':
            # Check if there's an attendance record with came_without_registration
            conn = sqlite3.connect('skud.db')
            cursor = conn.cursor()
            cursor.execute('SELECT status FROM attendance WHERE student_id = (SELECT id FROM students WHERE name = ?) AND meal_id = ?', (student_name, meal_id))
            attendance_status = cursor.fetchone()
            conn.close()
            if attendance_status and attendance_status[0] == 'came_without_registration':
                status = 'came_without_registration'
        records.append({
            'student_name': student_name,
            'meal_id': meal_id,
            'day_of_week': day_of_week,
            'meal_name': meal_name,
            'status': status
        })
    return records
