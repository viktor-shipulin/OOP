from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

    @abstractmethod
    def refund(self, amount):
        pass

class CreditCardPayment(Payment):
    def pay(self, amount):
        print("Оплата через карту:", amount)

    def refund(self, amount):
        print("Возврат на карту:", amount)

class CryptoPayment(Payment):
    def pay(self, amount):
        print("Оплата криптой:", amount)

    def refund(self, amount):
        print("Возврат криптой:", amount)

payments = [CreditCardPayment(), CryptoPayment()]

for p in payments:
    p.pay(1500)
    p.refund(500)


class Course(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def get_materials(self):
        pass

    @abstractmethod
    def end(self):
        pass


class PythonCourse(Course):
    def start(self):
        print("Курс Python начался")

    def get_materials(self):
        print("Материалы: синтаксис, ООП, модули, файлы")

    def end(self):
        print("Курс Python закончен")


class MathCourse(Course):
    def start(self):
        print("Курс Математики начался")

    def get_materials(self):
        print("Материалы: алгебра, геометрия, тригонометрия")

    def end(self):
        print("Курс Матемтики закончен")


courses = [PythonCourse(), MathCourse()]

for c in courses:
    c.start()
    c.get_materials()
    c.end()


class Delivery(ABC):
    @abstractmethod
    def calculate_cost(self, distance):
        pass

    @abstractmethod
    def deliver(self):
        pass


class AirDelivery(Delivery):
    def calculate_cost(self, distance):
        return distance * 105

    def deliver(self):
        print("Доставка по воздуху")


class GroundDelivery(Delivery):
    def calculate_cost(self, distance):
        return distance * 52

    def deliver(self):
        print("Доставка по земле")


class SeaDelivery(Delivery):
    def calculate_cost(self, distance):
        return distance * 38

    def deliver(self):
        print("Доставка по морю")


deliveries = [AirDelivery(), GroundDelivery(), SeaDelivery()]

for d in deliveries:
    print("Стоимость:", d.calculate_cost(120))
    d.deliver()


class BankAccount:
    def __init__(self, owner, balance, pin):
        self.owner = owner
        self.balance = balance
        self.pin = pin

    def deposit(self, amount, pin):
        if pin == self.pin and amount > 0:
            self.balance += amount
            print("Пополнено:", amount)
        else:
            print("Ошибка при пополнении")

    def withdraw(self, amount, pin):
        if pin == self.pin and 0 < amount <= self.balance:
            self.balance -= amount
            print("Снято:", amount)
        else:
            print("Ошибка при снятии")

    def change_pin(self, old_pin, new_pin):
        if old_pin == self.pin:
            self.pin = new_pin
            print("PIN изменён")
        else:
            print("Неверный старый PIN")


acc = BankAccount("Иван", 5000, 1234)
acc.deposit(1000, 1234)
acc.withdraw(600, 1234)
acc.change_pin(1234, 9999)


class UserProfile:
    def __init__(self, email, password, status="free"):
        self.email = email
        self.password = password
        self.status = status

    def login(self, email, password):
        if self.email == email and self.password == password:
            print("Вход выполнен")
        else:
            print("Ошибка! неверные данные")

    def upgrade_to_premium(self):
        self.status = "premium"
        print("Профиль стал премиум")

    def get_info(self):
        print("Email:", self.email, "Статус:", self.status)


user = UserProfile("test@mail.com", "12345")
user.login("test@mail.com", "12345")
user.upgrade_to_premium()
user.get_info()


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.__discount = 0

    def get_price(self):
        return self.price * (1 - self.__discount / 100)

    def set_discount(self, discount, is_admin=False):
        if is_admin:
            self.__discount = discount
            print("Скидка установлена", discount)
        else:
            print("Нет доступа")


p = Product("Ноутбук", 50000)
p.set_discount(10, is_admin=True)
print("Цена со скидкой:", p.get_price())


class TextFile:
    def open(self):
        print("Открыт текстовый файл")

class ImageFile:
    def open(self):
        print("Открыт файл изображения")

class AudioFile:
    def open(self):
        print("Открыт аудиофайл")

def open_all(files):
    for f in files:
        f.open()

files = [TextFile(), ImageFile(), AudioFile()]
open_all(files)


class Car:
    def move(self, distance):
        speed = 80
        time = distance / speed
        print("Машина проехала", distance, "км за", round(time,2), "час")

class Truck:
    def move(self, distance):
        speed = 60
        time = distance / speed
        print("Грузовик проехал", distance, "км за", round(time,2), "час")

class Bicycle:
    def move(self, distance):
        speed = 20
        time = distance / speed
        print("Велосипед проехал", distance, "км за", round(time,2), "час")

def simulate_transport(transport_list):
    for t in transport_list:
        t.move(120)

transport = [Car(), Truck(), Bicycle()]
simulate_transport(transport)


class Student:
    def access_portal(self):
        print("Студент видит расписание")

class Teacher:
    def access_portal(self):
        print("Преподаватель выставляет оценки")

class Administrator:
    def access_portal(self):
        print("Админ управляет пользователями")

users = [Student(), Teacher(), Administrator()]

for u in users:
    u.access_portal()