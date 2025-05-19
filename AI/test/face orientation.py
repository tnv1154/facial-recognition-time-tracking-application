

import os
import cv2
import time
import numpy as np

from AI.src.add_vietnamese_text import AddVietnameseText
from mtcnn import MTCNN

class FaceOrientation:
    def calculate_Angle(self, x, y, z):
        """Tính góc tạo bởi 3 điểm a, b, c"""
        # chuyển list thành numpy array
        a = np.array(x, dtype=np.float32)
        b = np.array(y, dtype=np.float32)
        c = np.array(z, dtype=np.float32)
        #tạo 2 vector ba, bc
        ba = a - b
        bc = c - b
        #tích góc tạo bởi 2 vector
        tich_2_vector = np.dot(ba, bc)
        len_ba = np.linalg.norm(ba)
        len_bc = np.linalg.norm(bc)
        cos = tich_2_vector / (len_ba * len_bc)
        goc_rad = np.arccos(cos)
        return np.degrees(goc_rad)

    def face_orientation_detection(self, detected_faces):
        """Phát hiện góc của khuôn mặt"""
        left_eye = detected_faces[0]['keypoints']['left_eye']
        right_eye = detected_faces[0]['keypoints']['right_eye']
        nose = detected_faces[0]['keypoints']['nose']

        goc_trai = self.calculate_Angle(right_eye, left_eye, nose)
        goc_phai = self.calculate_Angle(left_eye, right_eye, nose)

        if int(goc_phai) in range(40, 60) and int(goc_trai) in range(40, 60):
            face_orientation = "Front"
        else:
            if goc_phai < goc_trai:
                face_orientation = "Left"
            else:
                face_orientation = "Right"

        return face_orientation


def main():
    cap = cv2.VideoCapture(0)
    detector = MTCNN()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        small_frame = cv2.resize(frame, (0, 0), fx=0.4, fy=0.4)
        detected_faces = detector.detect_faces(small_frame)
        face_found = len(detected_faces)
        if face_found == 1:
            x, y, width, height = detected_faces[0]['box']
            cv2.rectangle(small_frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
            face_orientation = FaceOrientation().face_orientation_detection(detected_faces)
            cv2.putText(small_frame, face_orientation, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            left_eye = detected_faces[0]['keypoints']['left_eye']
            right_eye = detected_faces[0]['keypoints']['right_eye']
            nose = detected_faces[0]['keypoints']['nose']
            cv2.circle(small_frame, (left_eye[0], left_eye[1]), 2, (0, 0, 255), -1)
            cv2.circle(small_frame, (right_eye[0], right_eye[1]), 2, (0, 0, 255), -1)
            cv2.circle(small_frame, (nose[0], nose[1]), 2, (0, 0, 255), -1)

            cv2.line(small_frame, left_eye, right_eye, (0, 255, 0), 2)
            cv2.line(small_frame, right_eye, nose, (0, 255, 0), 2)
            cv2.line(small_frame, nose, left_eye, (0, 255, 0), 2)

        cv2.imshow("Face Detection", small_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()