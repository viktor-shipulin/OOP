import sqlite3

class Database:
        def __init__(self, db_name="todo.db"):
            self.connection = sqlite3.connect(db_name)
            self.cursor = self.connection.cursor()
            self.create_table()
        def create_table(self):
            self.cursor.execute(""" 
            
            CREATE TABLE NOT EXISTS todo(
                                id INGER PRIMARY KEY AUTOINCREMENT,
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