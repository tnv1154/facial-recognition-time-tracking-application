

import os
import cv2
import time
import numpy as np

from AI.src.add_vietnamese_text import AddVietnameseText
from mtcnn import MTCNN

class FaceOrientation:
    def __init__(self, face_point):
        self.detector = MTCNN()
        self.face_point = face_point

    def calculate_Angle(self, a, b, c):
        """Tính góc tạo bởi 3 điểm a, b, c"""
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

if __name__ == "__main__":
    main()