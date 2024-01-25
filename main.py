import copy
import csv
import itertools
import time

import cv2
import mediapipe as mp

from classifier import Classifier

classifier = Classifier()

meaningful_points = [2, 4, 5, 8, 9, 12, 13, 16, 17, 20]
# meaningful_points = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
#                      17, 18, 19, 20]
new_list = []
for i in meaningful_points:
    new_list.append(i * 2)
    new_list.append(i * 2 + 1)
meaningful_points = new_list


def logCsv(mode, landmark_list):
    if mode == 0:
        pass
    if mode == 1:
        csv_path = 'model/keypoint_ours.csv'
        with open(csv_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(landmark_list)
    return


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
    temp_landmark_list_select = [temp_landmark_list[i] for i in
                                 meaningful_points]

    return (temp_landmark_list_select, temp_landmark_list)


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
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame)
        classifier = Classifier()
        if result.multi_hand_landmarks:
            for landmark in result.multi_hand_landmarks:
                mode = 1 if cv2.waitKey(10) & 0xFF == ord('k') else 0
                (landmark_list, to_save) = calc_landmark_list(frame, landmark)
                classification_result = classifier(landmark_list)
                mpDraw.draw_landmarks(frame, landmark, mpHands.HAND_CONNECTIONS)
                logCsv(mode, to_save)
                if classification_result is None:
                    continue
                confidence, hand_sign_id = classification_result
                print(
                    f"Gesture detection result: {labels[hand_sign_id]} ({confidence})")
                cv2.putText(frame,
                            f"{labels[hand_sign_id]} ({round(confidence * 100, 2)}%)",
                            (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                            cv2.LINE_AA)

        cv2.imshow("Output", frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
