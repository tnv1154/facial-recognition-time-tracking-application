"""Cắt khuôn mặt"""

import os
import numpy as np
from mtcnn import MTCNN
from PIL import Image
face_path = "E:\PythonProjectMain\AI\DataSet\FaceData"
detector = MTCNN()

# Số pixel muốn mở rộng xung quanh khuôn mặt
MARGIN = 10

class ailgn_data:
    def __init__(self, id):
        crop_faces_for_id(id)

def crop_faces_for_id(id_name: str):
    raw_dir = os.path.join(face_path, "raw", id_name)
    processed_dir = os.path.join(face_path, "processed", id_name)

    # Tạo thư mục đích nếu chưa có
    os.makedirs(processed_dir, exist_ok=True)

    for i in range(1, 51):  # ảnh từ 001 đến 050

        file_name = f"{id_name}_{i:03}"
        input_path = os.path.join(raw_dir, f"{file_name}.png")
        output_path = os.path.join(processed_dir, f"{file_name}.png")

        if not os.path.exists(input_path):
            print(f"[WARN] Không tìm thấy ảnh: {input_path}")
            continue

        # Mở ảnh
        image = Image.open(input_path).convert("RGB")
        image_array = np.asarray(image)

        # Phát hiện khuôn mặt
        results = detector.detect_faces(image_array)

        if len(results) == 0:
            print(f"[WARN] Không phát hiện khuôn mặt: {file_name}")
            continue

        # Lấy bounding box của khuôn mặt đầu tiên
        x, y, width, height = results[0]['box']
        x_new = max(0, x - MARGIN)
        y_new = max(0, y - MARGIN)
        x2_new = min(image.width, x + width + MARGIN)
        y2_new = min(image.height, y + height + MARGIN)

        # Crop ảnh với bounding box có margin và giới hạn trong ảnh
        face = image.crop((x_new, y_new, x2_new, y2_new))

        # Resize về 182x182
        face = face.resize((182, 182))

        # Lưu ảnh
        face.save(output_path, format="PNG")
        print(f"[INFO] Đã xử lý: {file_name}.png  MARGIN : {MARGIN}")

def main():
    id = input("Nhap id: ")
    crop_faces_for_id(id)
    print("Done!")

if __name__ == "__main__":
    main()