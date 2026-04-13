import random

class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.num_bullets = random.randint(1, 3)
        self.bullet_positions = random.sample(range(1, 7), self.num_bullets)
        self.current_position = 1
        self.lives = 3
        self.alive = True

    def shot(self):
        if not self.alive:
            return "game_over"

        if self.current_position in self.bullet_positions:
            self.lives -= 1
            if self.lives <= 0:
                self.alive = False
                self.current_position += 1
                return "dead"
            self.current_position += 1
            return "boom"
        
        self.current_position += 1
        return "empty"