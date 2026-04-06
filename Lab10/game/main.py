from  game import first_challenge, riddle_challenge, final_challenge
import sys 

def main():
    player_name = input('Тебе нужно будет пройти испытание, чтобы выиграть в этой игре, но если проиграешь, то я тебя съем.\n Напиши свое имя!\n А если ты испугаешься и решишь сбежать, то просто скажи мне заклинание - exit: ')

    if player_name.lower() == "exit":
        print("Решил сбежать...")
        return
    else:
        print(f"Добро пожаловать, {player_name}!")


    first_challenge()
    
    riddle_challenge()
    
    final_challenge(player_name)
    
if __name__ == "__main__":
    main()