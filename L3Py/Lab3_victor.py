data_tuple = ('h', 6.13, 'C', 'e', 'T', True, 'k', 'e', 3, 'e', 1, 'g')
data_tuple = list(data_tuple)
letters = []
numbers = []

for i in data_tuple:
    if type(i) == str:
        letters.append(i)         
    else:
        numbers.append(i)

numbers.remove(6.13)

letters.append(True)
numbers.insert(1, 2)
numbers.sort()
letters.reverse()

letters[0] = 'C'
letters[1] = 'A'
letters[2] = 'K'
letters[3] = 'E'
del letters[4:]

letters_tuple = tuple(letters)
numbers_tuple = tuple(numbers)

print(letters_tuple)
print(numbers_tuple)