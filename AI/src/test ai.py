import cv2
from mtcnn import MTCNN

# Khởi tạo detector
detector = MTCNN()

# Mở webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # === ⚠️ Giảm độ phân giải ảnh đầu vào để tăng tốc độ ===
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) # Có thể thay bằng (480, 360)

    # Chuyển sang RGB (MTCNN dùng RGB)
    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Phát hiện khuôn mặt
    results = detector.detect_faces(rgb_frame)

    # Vẽ khung lên ảnh gốc (scale lại tọa độ)
    for result in results:
        x, y, width, height = result['box']
        confidence = result['confidence']

        # Scale tọa độ lên ảnh gốc
        scale_x = frame.shape[1] / small_frame.shape[1]
        scale_y = frame.shape[0] / small_frame.shape[0]

        x = int(x * scale_x)
        y = int(y * scale_y)
        w = int(width * scale_x)
        h = int(height * scale_y)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"{confidence:.2f}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Hiển thị
    cv2.imshow("Face Detection (MTCNN)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
