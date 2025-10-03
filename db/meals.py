import sqlite3
import datetime

def get_current_meal():
    now = datetime.datetime.now()
    current_time = now.time()
    current_day = now.weekday()  # Monday=0, Sunday=6
    conn = sqlite3.connect('skud.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, start_time, end_time, day_of_week FROM meals WHERE day_of_week = ?', (current_day,))
    meals = cursor.fetchall()
    conn.close()

    for meal_id, start_str, end_str, day_of_week in meals:
        start_time = datetime.datetime.strptime(start_str, '%H:%M').time()
        end_time = datetime.datetime.strptime(end_str, '%H:%M').time()
        if start_time <= current_time <= end_time:
            return meal_id
    return None

def get_meal_name(meal_id):
    conn = sqlite3.connect('skud.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM meals WHERE id = ?', (meal_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
