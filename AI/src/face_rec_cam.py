
from collections import Counter
import tensorflow as tf
import imutils
import os

import pickle
import numpy as np
import cv2

import time
from mtcnn import MTCNN
from AI.src import facenet
from AI.src.add_vietnamese_text import AddVietnameseText


IMAGE_SIZE = 160
INPUT_IMAGE_SIZE = 182
BASE_PATH = "E:/PythonProjectMain/AI"
CLASSIFIER_PATH = os.path.join(BASE_PATH, 'Models', 'classifier.pkl')
FACENET_MODEL_PATH = os.path.join(BASE_PATH, 'Models', '20180402-114759.pb')
MIN_FACE_HEIGHT_RATIO = 0.25

class FaceNetModel:
    def __init__(self):
        self.is_loaded = False
        self.model = None
        self.class_names = None
        self.graph = None
        self.sess = None
        self.images_placeholder = None
        self.embeddings = None
        self.phase_train_placeholder = None
        self.detector = None


    def start_model(self):
        """Tải mô hình """
        #Kiểm tra mô hình đã đc tải chưa
        if self.is_loaded:
            return

        print("Tải mô hình FaceNet...")
        start_time = time.time()

        #Tải mô hình classifier
        with open(CLASSIFIER_PATH, 'rb') as file:
            self.model, self.class_names = pickle.load(file)
        print("tải mô hình phân loại thành công")

        #Tải mô hình trích xuất đặc trưng
        self.graph = tf.compat.v1.Graph()
        with self.graph.as_default():
            #cấu hình session
            config = tf.compat.v1.ConfigProto(
                intra_op_parallelism_threads=4,  # Số luồng để tận dụng đa nhân CPU
                inter_op_parallelism_threads=2,  # Số luồng để tận dụng đa nhân CPU
                allow_soft_placement=True,  # Cho phép đặt op trên CPU nếu không có GPU
                device_count={'CPU': 4}  # Số lượng CPU được phép sử dụng
            )
            self.sess = tf.compat.v1.Session(config=config)
            with self.sess.as_default():
                #load model
                facenet.load_model(FACENET_MODEL_PATH)
                #lấy tensor
                self.images_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("input:0")
                self.embeddings = tf.compat.v1.get_default_graph().get_tensor_by_name("embeddings:0")
                self.phase_train_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("phase_train:0")
                self.embedding_size = self.embeddings.get_shape()[1]
                #load thư viện ntcnn

        self.detector = MTCNN()
        self.is_loaded = True
        end_time = time.time()
        print(f"Tải mô hình thành công trong : {end_time - start_time:.2f} giây")

class FaceRecognitionCam:
    def __init__(self):
        self.model = FaceNetModel()
        self.id_arr = []
        self.person_detected = Counter()

    def check_model_loaded(self):
        """kiểm tra mô hình đã đc tải chưa"""
        if not self.model.is_loaded:
            self.model.start_model()

    def process_frame(self, frame):
        """Xử lý từng frame"""
        detected_id = None
        if frame is None:
            return frame,
        frame = imutils.resize(frame, width=600)

        with self.model.graph.as_default():
            with self.model.sess.as_default():
                # Phát hiện khuôn mặt
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                detected_face = self.detector.detect_faces(small_frame)
                face_found = detected_face.shape[0]
                if face_found > 1:
                    frame = AddVietnameseText.add_vietnamese_text(frame, "Có nhiều hơn 1 khuôn mặt", (10, 30))
                elif face_found == 0:
                    frame = AddVietnameseText.add_vietnamese_text(frame, "Không phát hiện khuôn mặt", (10, 30))
                else:
                    x, y, width, height = detected_face['box']
                    x, y = max(0, x), max(0, y)

                    #bỏ qua khuôn mặt quá nhỏ
                    face_height_ratio = height / small_frame.shape[0]
                    if face_height_ratio > MIN_FACE_HEIGHT_RATIO:
                        #cắt khuôn mặt và resize
                        cropped = small_frame[y : y + height, x : x + width]
                        scaled = cv2.resize(cropped, (INPUT_IMAGE_SIZE, INPUT_IMAGE_SIZE))
                        chuan_hoa = facenet.chuan_hoa_anh(scaled)
                        reshaped = chuan_hoa.reshape(-1, INPUT_IMAGE_SIZE, INPUT_IMAGE_SIZE, 3)

                        #Tính vector đặc trưng
                        feed_dict = {self.model.images_placeholder: reshaped, self.model.phase_train_placeholder: False}
                        emb_arr = self.model.sess.run(self.model.embeddings, feed_dict=feed_dict)

                        #Nhận diện
                        predictions = self.model.model.predict_proba(emb_arr)
                        best_class_indices = np.argmax(predictions, axis=1)
                        best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]
                        best_name = self.model.class_names[best_class_indices[0]]
                        print("ID: {}, Độ chính xác: {}".format(best_name, best_class_probabilities))

                        if best_class_probabilities > 0.8:
                            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
                            cv2.putText()





