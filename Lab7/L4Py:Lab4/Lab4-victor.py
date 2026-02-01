flags = {
    'ru': {'red', 'blue', 'white'},
    'kg': {'red'},
    'ua': {'red', 'blue'},
    'uk': {'red', 'blue'},
    'kz': {'yellow', 'blue'},
    'arm': {'red', 'blue', 'orange'},
    'bah': {'red', 'white'}
}


while True:
    user = input('Введите цвета флагов или выйдите из программы - выход  ')

    if user == 'выход':
        break
    for country, colors in flags.items():
        if user in colors:
            print(country)
