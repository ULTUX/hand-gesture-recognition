import copy
import csv
import itertools

import cv2
import mediapipe as mp

from classifier import Classifier
print(mp.__file__)

def load_labels(path):
    with open(path, 'r') as f:
        return [line[0] for line in csv.reader(f)]


def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # Keypoint
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_point.append([landmark_x, landmark_y])

    temp_landmark_list = copy.deepcopy(landmark_point)
    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]
        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y
    # Convert to a one-dimensional list
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))
    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list


if __name__ == '__main__':
    mpHands = mp.solutions.hands
    mpDraw = mp.solutions.drawing_utils
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    labels = load_labels('model/labels.csv')
    print(labels)

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        classifier = Classifier()
        if result.multi_hand_landmarks:
            for landmark in result.multi_hand_landmarks:
                landmark_list = calc_landmark_list(frame, landmark)
                hand_sign_id = classifier(landmark_list)
                print(labels[hand_sign_id])
                cv2.putText(frame, labels[hand_sign_id], (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                            cv2.LINE_AA)
                mpDraw.draw_landmarks(frame, landmark, mpHands.HAND_CONNECTIONS)

        cv2.imshow("Output", frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
