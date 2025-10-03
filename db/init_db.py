import sqlite3
import datetime

def init_db():
    conn = sqlite3.connect('skud.db')
    conn.execute('PRAGMA foreign_keys = ON;')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            card_id INTEGER UNIQUE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL
        )
    ''')
    # Add day_of_week column if not exists
    try:
        cursor.execute('ALTER TABLE meals ADD COLUMN day_of_week INTEGER NOT NULL DEFAULT 0')
    except sqlite3.OperationalError:
        pass  # Column already exists

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY,
            student_id INTEGER,
            meal_id INTEGER,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (meal_id) REFERENCES meals (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY,
            student_id INTEGER,
            meal_id INTEGER,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL,  -- 'came' or 'didnt_come'
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (meal_id) REFERENCES meals (id)
        )
    ''')
    students = []
    
    cursor.executemany('INSERT OR IGNORE INTO students VALUES (?, ?, ?)', students)

    cursor.execute('DELETE FROM registrations')  # Clear old registrations
    cursor.execute('DELETE FROM attendance')  # Clear old attendance
    cursor.execute('DELETE FROM meals')  # Clear old meals
    meals = []
    for day in range(7):  # 0=Monday to 6=Sunday
        meals.extend([
            (None, 'Breakfast', '07:00', '09:00', day),
            (None, 'Lunch', '11:00', '14:00', day),
            (None, 'Dinner', '18:00', '20:00', day)
        ])
    cursor.executemany('INSERT INTO meals VALUES (?, ?, ?, ?, ?)', meals)

    registrations = []
    cursor.executemany('INSERT OR IGNORE INTO registrations VALUES (?, ?, ?)', registrations)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized.")
