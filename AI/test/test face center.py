import cv2
from mtcnn import MTCNN

# Hàm kiểm tra điểm có nằm trong elip không
def is_point_in_ellipse(center, axes, point):
    cx, cy = center
    a, b = axes
    x, y = point
    return ((x - cx) ** 2) / (a ** 2) + ((y - cy) ** 2) / (b ** 2) <= 1

# Hàm kiểm tra hình chữ nhật A nằm trong hình chữ nhật B
def is_rect_inside(rect_a, rect_b):
    ax, ay, aw, ah = rect_a
    bx, by, bw, bh = rect_b
    return (ax >= bx and ay >= by and
            ax + aw <= bx + bw and
            ay + ah <= by + bh)

# Khởi tạo MTCNN
detector = MTCNN()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (0, 0), fx=0.4, fy=0.4)
    h, w = frame.shape[:2]

    center_ellipse = (w // 2, h // 2)
    axes_ellipse = (w // 3, h // 4)  # hình elip cơ bản

    # --- Vẽ hình elip ---
    cv2.ellipse(frame, center_ellipse, axes_ellipse, 0, 0, 360, (0, 255, 0), 2)

    # --- Vẽ hình chữ nhật ngoài (chạm elip) ---
    scale_outer = 1.12  # tăng lên 120%
    outer_rect = (
        int(center_ellipse[0] - axes_ellipse[0] * scale_outer),
        int(center_ellipse[1] - axes_ellipse[1] * scale_outer),
        int(axes_ellipse[0] * 2 * scale_outer),
        int(axes_ellipse[1] * 2 * scale_outer)
    )

    cv2.rectangle(frame,
                  (outer_rect[0], outer_rect[1]),
                  (outer_rect[0] + outer_rect[2], outer_rect[1] + outer_rect[3]),
                  (0, 255, 255), 2)

    # --- Vẽ hình chữ nhật trong (4 đỉnh nằm trên elip) ---
    scale_inner = 0.5  # co nhỏ ít hơn → hình to hơn
    inner_rect = (
        int(center_ellipse[0] - axes_ellipse[0] * scale_inner),
        int(center_ellipse[1] - axes_ellipse[1] * scale_inner),
        int(axes_ellipse[0] * 2 * scale_inner),
        int(axes_ellipse[1] * 2 * scale_inner)
    )

    cv2.rectangle(frame,
                  (inner_rect[0], inner_rect[1]),
                  (inner_rect[0] + inner_rect[2], inner_rect[1] + inner_rect[3]),
                  (255, 0, 255), 2)

    # Phát hiện khuôn mặt
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(rgb)

    for face in faces:
        x, y, w_box, h_box = face['box']
        face_rect = (x, y, w_box, h_box)

        # Kiểm tra xem khuôn mặt nằm giữa hai hình chữ nhật
        def is_rect_between(rect, outer, inner):
            rx, ry, rw, rh = rect
            ox, oy, ow, oh = outer
            ix, iy, iw, ih = inner

            left   = rx
            right  = rx + rw
            top    = ry
            bottom = ry + rh

            outer_left   = ox
            outer_right  = ox + ow
            outer_top    = oy
            outer_bottom = oy + oh

            inner_left   = ix
            inner_right  = ix + iw
            inner_top    = iy
            inner_bottom = iy + ih

            return (
                outer_left <= left <= inner_left and
                outer_right >= right >= inner_right and
                outer_top <= top <= inner_top and
                outer_bottom >= bottom >= inner_bottom
            )

        if is_rect_between(face_rect, outer_rect, inner_rect):
            status = "Nam giua 2 hinh"
            color = (0, 255, 0)
        else:
            status = "Ngoai khoang trung tam"
            color = (0, 0, 255)

        # Vẽ khung khuôn mặt và thông báo
        cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), color, 2)
        cv2.putText(frame, status, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("Face in Ellipse & Rectangle", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
