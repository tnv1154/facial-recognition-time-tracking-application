import cv2
from mtcnn import MTCNN
from AI.src.face_center_check import check_face_in_ellipse

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
        x, y, w_box, h_box = face['box']
        face_box = (x, y, w_box, h_box)

        status, color, inner_rect, outer_rect, center_ellipse, axes_ellipse = check_face_in_ellipse(frame, face_box)

        # Vẽ khuôn mặt
        cv2.ellipse(frame, center_ellipse, axes_ellipse, 0, 0, 360, (0, 255, 0), 2)
        cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), color, 2)
        cv2.putText(frame, status, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        # Vẽ khung ngoài và trong
        cv2.rectangle(frame,
                      (outer_rect[0], outer_rect[1]),
                      (outer_rect[0] + outer_rect[2], outer_rect[1] + outer_rect[3]),
                      (0, 255, 255), 2)
        cv2.rectangle(frame,
                      (inner_rect[0], inner_rect[1]),
                      (inner_rect[0] + inner_rect[2], inner_rect[1] + inner_rect[3]),
                      (255, 0, 255), 2)

    cv2.imshow("Face Position Check", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
