while True:
    color = str(input('какой горит цвет?'))

    if color  == 'красный':
        print(f'Сейчас горит - {color} STOP')
    elif color  == 'желтый':
        print(f'Сейчас горит - {color} Warning')
    elif color == 'зеленый':
        print(f'Сейчас горит - {color} GO')
    else:
        print('Используй ПДД!')
    exit_ = str(input('Выйти?'))
    if exit_ == 'да':
        print('До свидания!')
        break
    else:
        continue
