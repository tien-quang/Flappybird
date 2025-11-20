import random

class AIPlayer:
    def __init__(self):
        # Chọn số ống AI có thể vượt trước khi chết (1-20)
        self.pipes_can_pass = random.randint(1, 20)
        self.pipes_passed = 0
        self.alive = True
        self.score = 0

    def update_score(self):
        if self.alive:
            self.pipes_passed += 1
            self.score += 1
            if self.pipes_passed >= self.pipes_can_pass:
                self.alive = False
