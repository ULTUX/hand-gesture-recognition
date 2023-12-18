import copy
import csv
import itertools

import cv2
import mediapipe as mp

from classifier import Classifier
from steering import keys
from steering.config import gesture_dict


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


run_recognition_thread = True


def recognition_thread_run():
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    labels = load_labels('model/labels.csv')
    classifier = Classifier()

    cap = cv2.VideoCapture(0)

    while run_recognition_thread and cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if not ret:
            continue
        result = hands.process(frame)
        if result.multi_hand_landmarks:
            for landmark in result.multi_hand_landmarks:
                landmark_list = calc_landmark_list(frame, landmark)
                classification_result = classifier(landmark_list)
                if classification_result is None:
                    continue
                confidence, hand_sign_id = classification_result
                fire_press_keys(hand_sign_id)
                print(f"Gesture detection result: {hand_sign_id}. {labels[hand_sign_id]} ({confidence})")

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def fire_press_keys(hand_sign_id):
    keys_to_press = gesture_dict.get(str(hand_sign_id + 1))
    if keys_to_press is not None:
        keys.press_keys(keys_to_press)
