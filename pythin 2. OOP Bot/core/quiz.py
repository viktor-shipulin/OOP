class Quiz:
    def __init__(self):
        self.questions = [
            {
                "question": "Столица Франции?",
                "option": ["Берлин", "Париж", "Лондон", "Рим"],
                "correct": "Париж"
            },
            {
                "question": "2 + 2 = ?",
                "option": ["3", "4", "5"],
                "correct": "4"
            },
            {
                "question": "Самый большой океан?",
                "option": ["Атлантический", "Тихий", "Индийский", "Антарктический"],
                "correct": "Тихий"
            }
        ]

    def get_question(self, index):
        if index < len(self.questions):
            return self.questions[index]
        return None

    def total_question(self):
        return len(self.questions)