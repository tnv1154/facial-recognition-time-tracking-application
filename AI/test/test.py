import numpy as np
from mtcnn import MTCNN
import time
import cv2

class FaceDirectionDetector:
    def __init__(self):
        self.detector = MTCNN()
        # Các ngưỡng để xác định hướng mặt
        self.direction_threshold = 0.2  # Ngưỡng để xác định quay trái hoặc phải
        # Tỷ lệ giảm kích thước frame để tăng tốc xử lý
        self.scale_factor = 0.5

    def calculate_face_direction(self, face_landmarks):
        """
        Tính toán hướng khuôn mặt dựa trên các điểm landmark
        Điều chỉnh cho hình ảnh đã được lật như gương
        """
        # Lấy các điểm landmark mắt trái, mắt phải và mũi
        left_eye = np.array(face_landmarks['left_eye'])
        right_eye = np.array(face_landmarks['right_eye'])
        nose = np.array(face_landmarks['nose'])

        # Tính khoảng cách từ mũi đến trung điểm của hai mắt
        eye_center = (left_eye + right_eye) / 2

        # Tính vị trí tương đối của mũi so với trung điểm mắt
        eye_width = np.linalg.norm(right_eye - left_eye)
        nose_deviation = (nose[0] - eye_center[0]) / eye_width

        # Điều chỉnh hướng mặt cho hình ảnh gương
        # Trong hình ảnh gương, hướng trái/phải bị đảo ngược
        if nose_deviation > self.direction_threshold:
            return "Quay phải"  # Đảo ngược từ trái sang phải
        elif nose_deviation < -self.direction_threshold:
            return "Quay trái"  # Đảo ngược từ phải sang trái
        else:
            return "Nhìn thẳng"

    def draw_face_info(self, frame, face, direction, scale_factor=1.0):
        """
        Vẽ thông tin khuôn mặt và hướng lên frame
        """
        # Điều chỉnh tọa độ box và landmarks nếu đã thay đổi kích thước frame
        box = face['box']
        x, y, w, h = [int(coord / scale_factor) for coord in box]

        # Vẽ khung xung quanh khuôn mặt
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 155, 255), 2)

        # Vẽ hướng mặt
        cv2.putText(frame, f"Huong: {direction}",
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Vẽ các điểm landmark (điều chỉnh tỷ lệ)
        landmarks = face['keypoints']
        for key, point in landmarks.items():
            adjusted_point = (int(point[0] / scale_factor), int(point[1] / scale_factor))
            cv2.circle(frame, adjusted_point, 2, (0, 0, 255), -1)

        return frame

    def process_frame(self, frame):
        """
        Xử lý từng frame, phát hiện khuôn mặt và xác định hướng
        """
        # Lấy kích thước frame gốc
        original_height, original_width = frame.shape[:2]

        # Giảm kích thước frame để tăng tốc xử lý
        small_frame = cv2.resize(frame, (0, 0), fx=self.scale_factor, fy=self.scale_factor)

        # Phát hiện khuôn mặt trên frame đã giảm kích thước
        faces = self.detector.detect_faces(small_frame)

        # Nếu có khuôn mặt
        for face in faces:
            if face['confidence'] > 0.9:  # Chỉ xử lý các khuôn mặt có độ tin cậy cao
                direction = self.calculate_face_direction(face['keypoints'])
                frame = self.draw_face_info(frame, face, direction, self.scale_factor)

        return frame

    def run_detection(self):
        """
        Chạy phát hiện hướng khuôn mặt qua webcam
        """
        # Khởi tạo webcam
        cap = cv2.VideoCapture(0)

        # Kiểm tra webcam có hoạt động không
        if not cap.isOpened():
            print("Không thể mở webcam")
            return

        # Bỏ qua các frame đầu tiên để webcam khởi động
        for _ in range(10):
            cap.read()

        while True:
            # Đọc frame từ webcam
            ret, frame = cap.read()

            if not ret:
                print("Không thể đọc frame từ webcam")
                break

            # Bắt đầu tính thời gian xử lý
            start_time = time.time()

            # Xử lý frame
            processed_frame = self.process_frame(frame)

            # Tính FPS
            fps = 1.0 / (time.time() - start_time)
            cv2.putText(processed_frame, f"FPS: {fps:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Hiển thị kết quả
            cv2.imshow('Face Direction Detection', processed_frame)

            # Nhấn 'q' để thoát
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Giải phóng tài nguyên
        cap.release()
        cv2.destroyAllWindows()


def main():
    face_detector = FaceDirectionDetector()
    face_detector.run_detection()


if __name__ == "__main__":
    main()