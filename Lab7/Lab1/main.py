player_name = input('Тебе нужно будет пройти испытание, чтобы выиграть в этой игре, но если проиграешь, то я тебя съем.\n Напиши свое имя!\n А если ты испугаешься и решишь сбежать, то просто скажи мне заклинание - exit: ')

if player_name.lower() == "exit":
    print("Решил сбежать...")
else:
    print(f"Добро пожаловать, {player_name}!")

    while True:
        number = input("Введи число от 1 до 9: ")
        if not number.isdigit():
            print("Это не число!")
            continue
        number = int(number)
        if 1 <= number <= 5:
            print("Ты прошёл!")
            break
        elif number == 6:
            print("Я почти тебя поймал...")
            break
        elif 7 <= number <= 9:
            print("Ты проиграл!")
            exit()
        else:
            print("Выбери число от 1 до 9")

    print("\nТеперь тебя ждут три загадки! Ответишь на 2 верно и я тебя пожалею")
    score = 0
    answer1 = input("Белый,но не сахар. Пушистый,но не птица. Нет ног, а идёт.").lower()
    if score == "снег":
        print("Правильно!")
        score += 1
    else:
        print("Неправильно! Правильный ответ: снег")

    answer2 = input("Страус может назвать себя птицей?").lower()
    if answer2 == "нет":
        print("Правильно!")
        score += 1
    else:
        print("Неправильно! Нет, страусы не умеют разговаривать")

    answer3 = input("Каких камней не бывает в речке?").lower()
    if answer3 == "Сухих":
        print("Правильно!")
        score += 1
    else:
        print("Неправильно! Сухих")

    if score < 2:
        print("Ты проиграл!")
        exit()

    final = input("Финал! Введи число от 1 до 9: ")
    if not final.isdigit():
        print("Это не число!")
    else:
        final = int(final)
        if final <= 1 and final <= 7:
            print(f"Поздравляю {player_name}! Ты выиграл!")
        else:
            print(f"Я тебя съел {player_name}!")
