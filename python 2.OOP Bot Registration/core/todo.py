class todo:
    def __init__(self, database):
        self.db = database

    def add(self, user_id, text):
        self.db.execute("INSERT INTO todo (user_id, text, is_done) VALUES (?, ?, 0)", (user_id, text))

    def get_all(self, user_id):
        return self.db.fetchall("SELECT id, text, is_done FROM todo WHERE user_id = ?", (user_id,))

    def mark_done(self, todo_id, user_id):
        self.db.execute("UPDATE todo SET is_done = 1 WHERE id = ? AND user_id = ?", (todo_id, user_id))

    def delete(self, todo_id, user_id):
        self.db.execute("DELETE FROM todo WHERE id = ? AND user_id = ?", (todo_id, user_id))