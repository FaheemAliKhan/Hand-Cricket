import random

class GameEngine:
    def __init__(self):
        self.player_score = 0
        self.ai_score = 0

        self.first_innings = True
        self.batting = None

        self.target = None
        self.game_over = False

    def toss(self):
        return random.choice(["player", "ai"])

    def set_batting(self, winner):
        self.batting = winner

    def play_turn(self, player_num, ai_num):

        if self.game_over:
            return "GAME OVER"

        # -------- FIRST INNINGS --------
        if self.first_innings:

            if self.batting == "player":

                if player_num == ai_num:
                    self.first_innings = False
                    self.target = self.player_score + 1
                    self.batting = "ai"
                    return "PLAYER OUT! AI CHASING"

                self.player_score += player_num
                return "PLAYER BATTING"

            else:  # AI batting first

                if player_num == ai_num:
                    self.first_innings = False
                    self.target = self.ai_score + 1
                    self.batting = "player"
                    return "AI OUT! YOUR TURN"

                self.ai_score += ai_num
                return "AI BATTING"

        # -------- SECOND INNINGS --------
        else:

            if self.batting == "player":

                if player_num == ai_num:
                    self.game_over = True
                    return "YOU OUT!"

                self.player_score += player_num

                if self.player_score >= self.target:
                    self.game_over = True
                    return "YOU WON!"

                return "YOU CHASING"

            else:  # AI batting second

                if player_num == ai_num:
                    self.game_over = True
                    return "AI OUT!"

                self.ai_score += ai_num

                if self.ai_score >= self.target:
                    self.game_over = True
                    return "AI WON!"

                return "AI CHASING"

    def is_game_over(self):
        return self.game_over

    def result(self):
        if self.player_score > self.ai_score:
            return "YOU WIN"
        elif self.player_score < self.ai_score:
            return "AI WINS"
        else:
            return "DRAW"
