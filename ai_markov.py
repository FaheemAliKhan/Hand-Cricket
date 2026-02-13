import random

class MarkovAI:
    def __init__(self):
        self.transitions = {i: {j: 1 for j in range(1,11)} for i in range(1,11)}
        self.last_move = None

    def update(self, player_move):
        if self.last_move is not None:
            self.transitions[self.last_move][player_move] += 1
        self.last_move = player_move

    def predict(self):
        if self.last_move is None:
            return random.randint(1,10)

        probs = self.transitions[self.last_move]
        return max(probs, key=probs.get)
