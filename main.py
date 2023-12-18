import copy
import csv
import itertools
import threading
import time

import cv2
import mediapipe as mp

from classifier import Classifier

classifier = Classifier()


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


def process_frame(frame, land_mark):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame)
    if result.multi_hand_landmarks:
        for landmark in result.multi_hand_landmarks:
            landmark_list = calc_landmark_list(frame, landmark)
            classification_result = classifier(landmark_list)
            hands_poss = landmark
            if classification_result is None:
                continue
            land_mark['label'] = labels[classification_result[1]]
            land_mark['confidence'] = classification_result[0]
            land_mark['landmarks'] = landmark
            confidence, hand_sign_id = classification_result
            print(
                f"Gesture detection result: {labels[hand_sign_id]} ({confidence})")
    return frame


if __name__ == '__main__':
    mpHands = mp.solutions.hands
    mpDraw = mp.solutions.drawing_utils
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    labels = load_labels('model/labels.csv')
    print(labels)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set the resolution
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame_rate = 5  # Set the frame rate
    prev = 0
    landmarks = {'label': None, 'confidence': 0, 'landmarks': None}

    while cap.isOpened():
        time_elapsed = time.time() - prev
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if time_elapsed > 1. / frame_rate:
            prev = time.time()
            threading.Thread(target=process_frame,
                             args=(frame, landmarks)).start()
        if landmarks['landmarks'] is not None:
            mpDraw.draw_landmarks(frame, landmarks['landmarks'],
                                  mpHands.HAND_CONNECTIONS)
        if landmarks['label'] is not None and landmarks['confidence'] != 0:
            cv2.putText(frame,
                        f"{landmarks['label']} ({round(landmarks['confidence'] * 100, 2)}%)",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                        cv2.LINE_AA)
        cv2.flip(frame, 1)
        cv2.imshow('Output', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
