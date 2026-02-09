import sqlite3

class DatabaseTodo:
    def __init__(self, db_name="todo.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS todo(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text TEXT,
                is_done INTEGER
            ) """)
        self.connection.commit()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetchall(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
class UniversityDB:
    def __init__(self, db_name="university.db"):        
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                full_name TEXT,
                age INTEGER,
                group_name TEXT,
                phone TEXT,
                email TEXT,
                github_link TEXT,
                programming_lang TEXT,
                experience TEXT,
                hobby TEXT
            ) 
        """)
        self.conn.commit()

    def add_student(self, data: dict):
        self.cursor.execute('''
            INSERT INTO students (  
                user_id, full_name, age, group_name, phone, email, 
                github_link, programming_lang, experience, hobby                                 
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['user_id'], data['full_name'], data['age'], data['group_name'],
            data['phone'], data['email'], data['github_link'], 
            data['programming_lang'], data['experience'], data['hobby']
        ))
        self.conn.commit()

    def close(self):
        self.conn.close()