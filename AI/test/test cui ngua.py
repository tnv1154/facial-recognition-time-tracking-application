
import cv2
from mtcnn import MTCNN
import numpy as np
import math

def angle_between(p1, p2):
    """Tính góc nghiêng giữa 2 điểm"""
    x1, y1 = p1
    x2, y2 = p2
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return angle

def is_looking_straight(landmarks):
    left_eye = landmarks['left_eye']
    right_eye = landmarks['right_eye']
    nose = landmarks['nose']
    mouth_left = landmarks['mouth_left']
    mouth_right = landmarks['mouth_right']

    # Roll: độ nghiêng đầu (góc giữa 2 mắt)
    roll = angle_between(left_eye, right_eye)

    # Yaw: mũi phải gần tâm hai mắt + miệng (cân đối trái phải)
    eye_center_x = (left_eye[0] + right_eye[0]) / 2
    mouth_center_x = (mouth_left[0] + mouth_right[0]) / 2
    face_center_x = (eye_center_x + mouth_center_x) / 2
    yaw = nose[0] - face_center_x  # lệch trái/phải

    # Pitch: độ cao giữa mắt và miệng so với mũi
    eye_avg_y = (left_eye[1] + right_eye[1]) / 2
    mouth_avg_y = (mouth_left[1] + mouth_right[1]) / 2
    pitch = (nose[1] - eye_avg_y) - (mouth_avg_y - nose[1])

    # Ngưỡng xác định nhìn thẳng
    return abs(roll) < 10 and abs(yaw) < 10 and abs(pitch) < 10, roll, yaw, pitch

detector = MTCNN()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break


    frame = cv2.resize(frame, (0, 0), fx=0.4, fy=0.4)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(rgb)

    for face in faces:
        x, y, w, h = face['box']
        keypoints = face['keypoints']

        is_straight, roll, yaw, pitch = is_looking_straight(keypoints)

        color = (0, 255, 0) if is_straight else (0, 0, 255)
        label = "Dang nhin thang" if is_straight else "Khong nhin thang"
        cv2.putText(frame, f"{label}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        # Vẽ điểm đặc trưng
        for name, point in keypoints.items():
            cv2.circle(frame, point, 3, (255, 0, 0), -1)

        # Hiển thị giá trị góc
        cv2.putText(frame, f"Roll: {roll:.1f}", (x, y + h + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)
        cv2.putText(frame, f"Yaw: {yaw:.1f}", (x, y + h + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)
        cv2.putText(frame, f"Pitch: {pitch:.1f}", (x, y + h + 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)

    cv2.imshow("MTCNN Head Check", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):  # ESC
        break

cap.release()
cv2.destroyAllWindows()
