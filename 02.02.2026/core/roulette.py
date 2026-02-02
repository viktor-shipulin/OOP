
import random

class RussianRouletGame:
    def __init__(self):
        self.players = ["Алекс", "Макс"]
        self.current_player = 0

        self.chambers = [0, 0, 0, 0, 0, 1]
        random.shuffle(self.chambers)

        self.current_index = 0
        self.is_active = True

    def get_current_player(self):
        return self.players[self.current_player]

    def next_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def shoot(self):
        if not self.is_active:
            return "game_over"

        result = self.chambers[self.current_index]
        self.current_index += 1

        if result == 1:
            self.is_active = False
            return "boom"

        self.next_player()
        return "click"

    def timeout(self):
        self.is_active = False
        return "timeout"
