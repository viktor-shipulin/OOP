# num = int(input("Введите число"))
# if num % 2 == 0:
#     print("Чётное")
# else:
#     print("Нечётное")


# # # num1 = int(input("Введите первое число"))
# # # num2 = int(input("Введите второе число"))
# # # num3 = int(input("Введите третье число"))
# # # m = num1
# # # if num2 < m:
# # #     m = num2
# # # if num3 < m:
# # #     m = num3
# # # print("Самое маленькое число:", m)


# # # # i = (input("Введите число"))
# # # # for i in range(1, 11):
# # # #     print("5 *", i, "=", 5 * i)



# # # userintput = input("Введите строку: ")
# # # letters = "аеёиоуыэюяАЕЁИОУЫЭЮЯ"
# # # count = 0
# # # for i in userintput:
# # #     if i in letters:
# # #         count = count + 1
# # # print("Гласных", count)


# # # list = [1, 2, 3, 2, 4, 1, 5, 3]
# # # newlist = []
# # # for i in list:
# # #     if i not in newlist:
# # #         newlist.append(i)
# # # print(newlist)

# # students = {}
# # students["Jhon"] = 4
# # students["Sara"] = 5
# # students["Ivan"] = 3

# # sum = 0
# # for i in students:
# #     sum = sum + students[i]
# # aver = sum / len(students)

# # print("Оценка выше средней")
# # for name in students:
# #     if students[name] > aver:
# #         print(name)


# class BankAccount:
#     def __init__(self):
#         self.balance = 0  
#     def deposit(self, money):
#         self.balance = self.balance + money  
#     def withdraw(self, money):
#         if money <= self.balance:
#             self.balance = self.balance - money
#         else:
#             print("Недостаточно денег на счете")

#     def show_balance(self):
#         print("Ваш баланс ", self.balance)


# # age = int(input("Напишите сколько вам лет"))
# # print("Через год вам будет", age + 1)



# letters = ["а", "е", "ё", "и", "о", "у", "ы", "э", "ю", "я"]
# userinput = input("Введите буквы")
# count = 0
# for i in userinput:
#     if i in letters:
#         count = count + 1

# print("Гласные", count)


