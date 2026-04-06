class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Mammal(Animal):
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color

class Reptile(Animal):
    def __init__(self, name, age, poison):
        super().__init__(name, age)
        self.poison = poison

class Zoo_show:
    def __init__(self):
        self.tiger_show = "Шоу с тиграми"
        self.snake_show = "Шоу с змеями"
        self.lion_show = "Шоу с львами"

    def info(self):
        print("Шоу которые есть в цирке ")
        print("1.", self.tiger_show)
        print("2.", self.snake_show)
        print("3.", self.lion_show)

    def tickets(self, price):
        if price == 1:
            print("Билет на шоу с тиграми. Цена 300 сом")
        elif price == 2:
            print("Билет на шоу со змеями. Цена 100 сом")
        elif price == 3:
            print("Билет на шоу с львами. Цена 200 сом")

tiger = Mammal("Тигр", 4, "оранжевый")
snake = Reptile("Кобра", 2, True)

zoo = Zoo_show()
zoo.info()
price = int(input("Введите номер шоу: "))
zoo.tickets(price)

