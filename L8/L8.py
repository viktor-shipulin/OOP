#Икапсуляция, полиморфизм, абстрации 

#инкапсюлцяи защита от прямого доступа. обьет самр решает какие данные открывать а какие нет 

# class BankAccount:
#     def __init__(self, name, balance):
#         self.name = name 
#         self.__balance = balance # два подчеркивания делает приватность 

#     def deposti(self, amount):
#         if amount > 0:
#             self.__balance += amount
#     def withdraw(self, amount):
#         if 0 <= amount: 
#             self.__balanceself-= amount 
#     def get_balance(self):
#         return self.__balance
    
# acc = BankAccount('Ivan', 1000)
# print(acc.name)
# print(acc.deposti(500))
# print(acc.get_balance)

#Абстрация - выделение более важных меодов атрибута. Мы используем готовый модуль абс. мы делали самые важные моменты в виде радуса и ширины 
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod #это называет дикоратор 
    def area():
        pass 
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius 
    def area(self):
        return 3.14 * self.radius **2 
    
class Rectangler(Shape):
    def __init__(self, width, height):
        self,width = width 
        self.height = height
    def area(self):
        return self.width * self.height 

 #еще способ как вызвать метод дописать из его кода 

 #полиморфизм это разное по смыслу но использует одно и тоже. Разные по смыслу но дейсвие одно и тоже. 
 # Например 
class Bird:
    def make_sound(self):
        print("Чирик-чирик")
class Cow:
    def make_sound(self):
        print('Moo-Moo')
animals = [Bird(), Cow()]
for animal in animals:
    animal.make_sound()
