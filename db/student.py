import sqlite3
import datetime

def finding_card(card_id):
    conn = sqlite3.connect('skud.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM students WHERE card_id = ?', (card_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def student_sheet(student_id, meal_id):
    conn = sqlite3.connect('skud.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM registrations WHERE student_id = ? AND meal_id = ?', (student_id, meal_id))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def check_student(card_id, meal_id):
    student_id = finding_card(card_id)
    if student_id is None:
        return 'unknown_card'
    registration = student_sheet(student_id, meal_id)
    if registration is not None:
        return 'registered'
    else:
        return 'not_registered'

def log_attendance(student_id, meal_id, status):
    conn = sqlite3.connect('skud.db')
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute('INSERT INTO attendance (student_id, meal_id, timestamp, status) VALUES (?, ?, ?, ?)',
                   (student_id, meal_id, timestamp, status))
    conn.commit()
    conn.close()

def add_student(name, card_id, group_name=None):
    conn = sqlite3.connect('skud.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name, card_id, group_name) VALUES (?, ?, ?)', (name, card_id, group_name))
    conn.commit()
    conn.close()

def add_registration(student_id, meal_id):
    conn = sqlite3.connect('skud.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO registrations (student_id, meal_id) VALUES (?, ?)', (student_id, meal_id))
    conn.commit()
    conn.close()

def get_all_students():
    conn = sqlite3.connect('skud.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, card_id, group_name FROM students')
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_student(student_id, name=None, card_id=None, group_name=None):
    conn = sqlite3.connect('skud.db')
    cursor = conn.cursor()
    if name:
        cursor.execute('UPDATE students SET name = ? WHERE id = ?', (name, student_id))
    if card_id:
        cursor.execute('UPDATE students SET card_id = ? WHERE id = ?', (card_id, student_id))
    if group_name:
        cursor.execute('UPDATE students SET group_name = ? WHERE id = ?', (group_name, student_id))
    conn.commit()
    conn.close()

def find_student_by_name_group(name, group_name):
    conn = sqlite3.connect('skud.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM students WHERE name = ? AND group_name = ?', (name, group_name))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def find_student_by_name(name):
    conn = sqlite3.connect('skud.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM students WHERE name = ?', (name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def delete_student(student_id):
    conn = sqlite3.connect('skud.db')
    conn.execute('PRAGMA foreign_keys = ON;')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM registrations WHERE student_id = ?', (student_id,))
    cursor.execute('DELETE FROM attendance WHERE student_id = ?', (student_id,))
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()
