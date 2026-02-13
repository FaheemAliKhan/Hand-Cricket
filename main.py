import cv2
import time
from hand_detector import HandDetector
from ai_markov import MarkovAI
from game_engine import GameEngine

cap = cv2.VideoCapture(0)

detector = HandDetector()
ai = MarkovAI()
game = GameEngine()

# Toss
toss_winner = game.toss()
game.set_batting(toss_winner)

last_move_time = 0
player_num = None
ai_num = None
message = "Game Started"

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    number = detector.get_number(frame)
    current_time = time.time()

    if number and current_time - last_move_time > 1 and not game.is_game_over():
        last_move_time = current_time

        player_num = number
        ai_num = ai.predict()
        ai.update(player_num)

        message = game.play_turn(player_num, ai_num)


    # ---------------- UI ----------------

    cv2.rectangle(frame, (0,0), (640,120), (0,0,0), -1)

    cv2.putText(frame, f"You: {game.player_score}", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.putText(frame, f"AI: {game.ai_score}", (350,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    if player_num:
        cv2.putText(frame, f"Your Throw: {player_num}", (20,90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    if ai_num:
        cv2.putText(frame, f"AI Throw: {ai_num}", (350,90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.putText(frame, f"Batting: {game.batting.upper()}", (180,115),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

    cv2.putText(frame, message, (250,150),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

    if game.is_game_over():
        cv2.putText(frame, game.result(), (180,250),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 3)

    cv2.imshow("Hand Cricket", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
