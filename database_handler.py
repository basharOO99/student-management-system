import sqlite3

class DatabaseHandler:
    DB_NAME = 'student.db'

    @staticmethod
    def _connect():
        return sqlite3.connect(DatabaseHandler.DB_NAME)
       
    @staticmethod
    def create_table():
        
        with DatabaseHandler._connect() as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL
            )''')

    @staticmethod
    def insert_student(name, email, age, gender):
       
        with DatabaseHandler._connect() as conn:
            conn.execute('''INSERT INTO students (name, email, age, gender)
                            VALUES (?, ?, ?, ?)''', (name, email, age, gender))

    @staticmethod
    def get_all_students():
        
        with DatabaseHandler._connect() as conn:
            return conn.execute('SELECT * FROM students').fetchall()

    @staticmethod
    def get_gender_count():
        
        with DatabaseHandler._connect() as conn:
            result = conn.execute('SELECT gender, COUNT(*) FROM students GROUP BY gender').fetchall()
            return dict(result)  


DatabaseHandler.create_table()
