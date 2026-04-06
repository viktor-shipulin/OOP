class Quiz:
    def __init__(self):
        self.questions = [
            {
                "question": "Какая планета самая большая в Солнечной системе?", 
                "option": ["Марс", "Юпитер", "Сатурн"], 
                "correct": "Юпитер",
                "image": "images/1.jpg"
            },
            {
                "question": "Кто написал 'Гарри Поттера'?", 
                "option": ["Толкин", "Роулинг", "Кинг"], 
                "correct": "Роулинг",
                "image": "images/2.jpeg"
            },
            {
                "question": "Самое глубокое озеро в мире?", 
                "option": ["Байкал", "Виктория", "Танганьика"], 
                "correct": "Байкал", 
                "image": "images/3.jpeg"
            },
            {
                "question": "Химический символ золота?", 
                "option": ["Ag", "Fe", "Au"], 
                "correct": "Au", 
                "image": "images/4.jpg"
            },
            {
                "question": "В какой стране находится пирамида Хеопса?", 
                "option": ["Греция", "Египет", "Мексика"], 
                "correct": "Египет", 
                "image": "images/5.jpeg"
            },
            {
                "question": "Сколько материков на Земле?", 
                "option": ["5", "6", "7"], 
                "correct": "6", 
                "image": "images/6.jpg"
            },
            {
                "question": "Кто нарисовал 'Мону Лизу'?", 
                "option": ["Пикассо", "Да Винчи", "Ван Гог"], 
                "correct": "Да Винчи", 
                "image": "images/7-7.jpg"
            },
            {
                "question": "Какой газ мы вдыхаем для жизни?", 
                "option": ["Азот", "Углекислый газ", "Кислород"], 
                "correct": "Кислород",
                "image": "images/8.webp"
            },
            {
                "question": "Самый быстрый зверь на планете?", 
                "option": ["Лев", "Гепард", "Сокол"], 
                "correct": "Гепард", 
                "image": "images/9.jpeg"
            },
            {
                "question": "В каком году человек впервые полетел в космос?", 
                "option": ["1957", "1961", "1969"], 
                "correct": "1961", 
                "image": "images/10-1.webp"
            },
            {
                "question": "Столица Японии?", 
                "option": ["Пекин", "Сеул", "Токио"], 
                "correct": "Токио", 
                "image": "images/10.webp"
            },
            {
                "question": "Какое животное изображено на логотипе Ferrari?", 
                "option": ["Бык", "Конь", "Ягуар"], 
                "correct": "Конь", 
                "image": "images/11-1.jpeg"
            },
            {
                "question": "Самая длинная река в мире?", 
                "option": ["Амазонка", "Нил", "Волга"], 
                "correct": "Амазонка", 
                "image": "images/12-1.jpeg"
            },
            {
                "question": "Сколько секунд в одном часе?", 
                "option": ["1000", "3600", "60"], 
                "correct": "3600", 
                "image": "images/13-1.jpg"
            },
            {
                "question": "На каком языке говорят в Бразилии?", 
                "option": ["Испанский", "Португальский", "Бразильский"], 
                "correct": "Португальский", 
                "image": "images/14-1.png"
            }
        ]

    def get_question(self, index):
        if index < len(self.questions):
            return self.questions[index]
        return None

    def total_questions(self):
        return len(self.questions)