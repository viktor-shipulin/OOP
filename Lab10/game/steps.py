def get_number_input(message):
    while True:
        user_input = input(message)
        
        if not user_input.isdigit():
            print("Это не число")
            continue
        
        return int(user_input)