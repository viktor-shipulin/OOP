class Account:
    def __init__(self, name, balance, acc_number, pin):
        self.name = name
        self.__balance = balance
        self.__acc_number = acc_number
        self.__pin = pin

    def deposit(self, amount, pin):
        if pin == self.__pin:
            self.__balance += amount
            print("Пополнено на", amount)
        else:
            print("PIN неверный")

    def withdraw(self, amount, pin):
        if pin == self.__pin:
            if amount <= self.__balance:
                self.__balance -= amount
                print("Снято", amount, "Баланс:", self.__balance)
            else:
                print("Недостаточно денег")
        else:
            print("PIN неверный")

    def get_balance(self, pin):
        if pin == self.__pin:
            print("Баланс:", self.__balance)
            return self.__balance
        else:
            print("PIN неверный")

acc = Account("Иван", 1000, 1234, 4321)
acc.deposit(500, 4321)
acc.withdraw(200, 4321)
acc.get_balance(4321)
acc.get_balance(1111)


class Product:
    def __init__(self, name, price):
        self.name = name
        self.__price = price

    def set_discount(self, percent):
        self.__price -= self.__price * percent/100
        if self.__price < 0: self.__price = 0

    def final_price(self):
        return self.__price

p = Product("Телефон", 1000)
print("До скидки:", p.final_price())
p.set_discount(20)
print("После скидки 20%:", p.final_price())


class SmartWatch:
    def __init__(self, battery):
        self.__battery = battery

    def use(self, minutes):
        self.__battery -= minutes/10
        if self.__battery < 0: self.__battery = 0
        print("Использовано", minutes, "минут, заряд:", self.__battery, "%")

    def charge(self, percent):
        self.__battery += percent
        if self.__battery > 100: self.__battery = 100
        print("Зарядили на", percent, "%. Сейчас:", self.__battery)

    def get_battery(self):
        return self.__battery

w = SmartWatch(50)
w.use(30)
w.charge(40)
print("Текущий заряд:", w.get_battery())


class Transport:
    def __init__(self, speed, capacity):
        self.speed = speed
        self.capacity = capacity

    def travel_time(self, distance):
        return distance/self.speed

class Bus(Transport): pass
class Train(Transport): pass

class Airplane(Transport):
    def travel_time(self, distance):
        return super().travel_time(distance)*0.8

bus = Bus(60, 50)
train = Train(120, 200)
plane = Airplane(800, 180)
distance = 240

print("Автобус:", bus.travel_time(distance))
print("Поезд:", train.travel_time(distance))
print("Самолет:", plane.travel_time(distance))


class Order:
    def __init__(self, amount):
        self.amount = amount
    def calculate_total(self):
        return self.amount

class DineInOrder(Order):
    def calculate_total(self):
        return self.amount*1.1

class TakeAwayOrder(Order):
    def calculate_total(self):
        return self.amount

class DeliveryOrder(Order):
    def calculate_total(self):
        return self.amount*1.1

orders = [DineInOrder(100), TakeAwayOrder(50), DeliveryOrder(200)]
for o in orders:
    print(o.calculate_total())


class Character:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

class Warrior(Character):
    def attack_enemy(self):
        print(self.name, "удар мечом!")

class Mage(Character):
    def attack_enemy(self):
        print(self.name, "кидает заклинание!")

class Archer(Character):
    def attack_enemy(self):
        print(self.name, "стреляет из лука!")

chars = [Warrior("Варвар",100,20), Mage("Маг",80,25), Archer("Лучник",90,15)]
for c in chars:
    c.attack_enemy()


class MediaFile:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

class AudioFile(MediaFile):
    def play(self):
        print(self.name, "играет аудио")

class VideoFile(MediaFile):
    def play(self):
        print(self.name, "видео воспроизводится")

class Podcast(MediaFile):
    def play(self):
        print(self.name, "слушаем эпизод")

files = [AudioFile("Песня",3), VideoFile("Фильм",120), Podcast("Подкаст",60)]
for f in files:
    f.play()


class PaymentSystem:
    def process_payment(self, amount): pass

class CreditCardPayment(PaymentSystem):
    def process_payment(self, amount): print("Картой:", amount)
class CryptoPayment(PaymentSystem):
    def process_payment(self, amount): print("Крипто:", amount)
class BankTransfer(PaymentSystem):
    def process_payment(self, amount): print("Банк:", amount)

payments = [CreditCardPayment(), CryptoPayment(), BankTransfer()]
for p in payments: p.process_payment(100)


class Animal:
    def eat(self): pass
    def sleep(self): pass

class Lion(Animal):
    def eat(self): print("Лев ест мясо")
    def sleep(self): print("Лев спит")

class Elephant(Animal):
    def eat(self): print("Слон ест траву")
    def sleep(self): print("Слон спит")

class Snake(Animal):
    def eat(self): print("Змея ест")
    def sleep(self): print("Змея свернулась и спит")


class Document:
    def open(self): pass
    def edit(self): pass
    def save(self): pass

class WordDocument(Document):
    def open(self): print("Word открыт")
    def edit(self): print("Редактируем Word")
    def save(self): print("Сохранили Word")

class PdfDocument(Document):
    def open(self): print("PDF открыт")
    def edit(self): print("PDF редактировать нельзя")
    def save(self): print("PDF сохранен")

class SpreadsheetDocument(Document):
    def open(self): print("Excel открыт")
    def edit(self): print("Редактируем Excel")
    def save(self): print("Сохранили Excel")


class Lesson:
    def start(self): pass

class VideoLesson(Lesson):
    def start(self): print("Старт видео урока")
class QuizLesson(Lesson):
    def start(self): print("Старт теста")
class TextLesson(Lesson):
    def start(self): print("Старт текстового урока")


class EmailNotification:
    def send(self,msg): print("Email:", msg)
class SMSNotification:
    def send(self,msg): print("SMS:", msg)
class PushNotification:
    def send(self,msg): print("Push:", msg)

notifs = [EmailNotification(), SMSNotification(), PushNotification()]
for n in notifs: n.send("Привет!")


class Square:
    def __init__(self,a): self.a=a
    def perimeter(self): return 4*self.a
class Circle:
    def __init__(self,r): self.r=r
    def perimeter(self): return 2*3.14*self.r
class Triangle:
    def __init__(self,a,b,c): self.a,self.b,self.c=a,b,c
    def perimeter(self): return self.a+self.b+self.c

shapes = [Square(5), Circle(3), Triangle(3,4,5)]
for s in shapes: print(s.perimeter())


class Manager:
    def work(self): print("Менеджер что-то делает")
class Developer:
    def work(self): print("Разработчик кодит")
class Designer:
    def work(self): print("Дизайнер рисует")

emps = [Manager(), Developer(), Designer()]
for e in emps: e.work()


class FireSpell:
    def cast(self,target): print("Огонь по",target)
class IceSpell:
    def cast(self,target): print("Заморозка на",target)
class HealingSpell:
    def cast(self,target): print("Лечим",target)

spells = [FireSpell(), IceSpell(), HealingSpell()]
for s in spells: s.cast("врагу")