import cv2
import mediapipe as mp

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
hands = mpHands.Hands(max_num_hands=2, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if result.multi_hand_landmarks:
        for landmark in result.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, landmark, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Output", frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
