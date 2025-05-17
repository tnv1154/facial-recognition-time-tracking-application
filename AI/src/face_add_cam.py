
import tensorflow as tf
import imutils
import os
import sys
import cv2
import time
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from tensorflow.python.distribute.device_util import current

from AI.src import facenet
from AI.src.add_vietnamese_text import AddVietnameseText
from mtcnn import MTCNN
from AI.src.align_data_mtcnn import ailgn_data
from AI.src.classifier import Classifier

Base_path = "E:/PythonProjectMain/AI"
print(f"Thư mục gốc : {Base_path}")
# Đường dẫn thư mục
RAW_FOLDER = os.path.join(Base_path, "DataSet", "FaceData", "raw")
PROCESSED_FOLDER = os.path.join(Base_path, "DataSet", "FaceData", "processed")
MODEL_PATH = os.path.join(Base_path, "Models", "20180402-114759.pb")
OUTPUT_CLASSIFIER = os.path.join(Base_path, "Models", "classifier.pkl")
# Thông số camera và ảnh
IMAGE_WIDTH = 480
IMAGE_HEIGHT = 640
DISPLAY_SCALE = 0.7  # Tỷ lệ hiển thị camera (70%)
NUM_IMAGES = 50
CAPTURE_INTERVAL = 0.25  # khoảng cách chụp giữa mỗi ảnh
CAMERA_INDEX = 0

class FaceAdd:
    def __init__(self, id_employee):
        self.face_add = main(id_employee)

def main(id_employee):
    """Thêm mới nhân viên"""
    #nhập id nhân viên
    person_id = id_employee
    person_folder = os.path.join(RAW_FOLDER, person_id)
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)
    else:
        print(f"Thư mục cho id {person_folder} đã tồn tại")
        overwrite = input("Tiếp tục và ghi đè dữ liệu (y/n): ")
        if overwrite.lower() != "y":
            print("Hủy thao tác")
            return

    print(f"Chuẩn bị chụp {NUM_IMAGES} ảnh cho id {person_id}...")
    print("Bắt đầu chụp...")
    print("Nhấn q để thoát")

#Khởi tạo mô hình

    #khởi tạo mtcnn
    detector = MTCNN()
    #khời tạo camera
    cap = cv2.VideoCapture(CAMERA_INDEX)
    time.sleep(2)

    count = 0
    last_capture_time = time.time()

    #Tính kích thức hiển thị
    display_width = int(IMAGE_WIDTH * DISPLAY_SCALE)
    display_height = int(IMAGE_HEIGHT * DISPLAY_SCALE)

    #Chụp ảnh
    while count < NUM_IMAGES:
        ret, frame = cap.read()
        if not ret:
            print("Không thể đọc frame từ camera")
            continue
        #frame = imutils.resize(frame, width=IMAGE_WIDTH)
        frame = cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT))
        small_frame = cv2.resize(frame, (0, 0), fx=0.4, fy=0.4)
        save_frame = frame.copy()
        #phát hiện khuôn mặt
        face_found = detector.detect_faces(small_frame)
        num_face = len(face_found)
        current_time = time.time()

        #Vẽ hình
        if num_face == 0:
            frame = AddVietnameseText.add_vietnamese_text(frame, "Không phát hiện khuôn mặt", (10, 30), font_size = 50, font_color = (255, 0, 0))
        elif num_face > 1:
            frame = AddVietnameseText.add_vietnamese_text(frame, "Có nhiều hơn 1 khuôn mặt trong khung hình", (10, 30), font_size = 50, font_color = (255, 0, 0))
        else:
            x, y, width, height = face_found[0]['box']
            scale_factor = 1 / 0.4  # Để phù hợp với fx=0.4, fy=0.4 bên trên
            x, y = max(0, int(x * scale_factor)), max(0, int(y * scale_factor))
            width, height = int(width * scale_factor), int(height * scale_factor)
            #x, y = max(0, int(x)), max(0, int(y))
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
            #Chụp ảnh sau mỗi khoảng thời gian
            if current_time - last_capture_time >= CAPTURE_INTERVAL and count < NUM_IMAGES:
                #lưu ảnh
                image_path = os.path.join(person_folder, f"{person_id}_{count + 1:03}.png")
                cv2.imwrite(image_path, save_frame)
                count += 1
                last_capture_time = current_time
                print(f"Đã chụp {count}/{NUM_IMAGES} ảnh")
            #thêm thông báo chụp ảnh
            frame = AddVietnameseText.add_vietnamese_text(frame, f"Đã chụp {count}/{NUM_IMAGES} ảnh", (10, 30), font_size = 50, font_color = (0, 255, 0))

        #Resize frame để hiển thị
        width = int(frame.shape[1] * DISPLAY_SCALE)
        height = int(frame.shape[0] * DISPLAY_SCALE)
        new_size = (width, height)
        resized_frame = cv2.resize(frame, new_size)

        #Hiển thị frame
        cv2.imshow("Face add", resized_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    print("Chụp ảnh hoàn tất")

    #Tiến hành cắt khuôn mặt
    print("Cắt khuôn mặt...")
    ailgn_data(person_id)
    print("Cắt khuôn mặt hoàn tất")

    #Tiến hành trích xuất đặc trung và huấn luyện bộ phân loại
    print("Huấn luyện bộ phân loại...")
    Classifier(PROCESSED_FOLDER, MODEL_PATH, OUTPUT_CLASSIFIER)

    print("Thêm mới nhân viên hoàn tất")

if __name__ == "__main__":
    FaceAdd(str(input("Nhập id nhân viên: ")))

