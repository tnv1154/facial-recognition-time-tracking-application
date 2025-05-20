import cv2

def check_face_in_ellipse(frame, face_box):
    h, w = frame.shape[:2]

    # Xác định hình elip trung tâm
    center_ellipse = (w // 2, h // 2)
    axes_ellipse = (w // 3, h // 4)

    # Khung ngoài (bao quanh elip)
    scale_outer = 1.12
    outer_rect = (
        int(center_ellipse[0] - axes_ellipse[0] * scale_outer),
        int(center_ellipse[1] - axes_ellipse[1] * scale_outer),
        int(axes_ellipse[0] * 2 * scale_outer),
        int(axes_ellipse[1] * 2 * scale_outer)
    )

    # Khung trong (nằm gọn trong elip)
    scale_inner = 0.5
    inner_rect = (
        int(center_ellipse[0] - axes_ellipse[0] * scale_inner),
        int(center_ellipse[1] - axes_ellipse[1] * scale_inner),
        int(axes_ellipse[0] * 2 * scale_inner),
        int(axes_ellipse[1] * 2 * scale_inner)
    )

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

    if is_rect_between(face_box, outer_rect, inner_rect):
        return "Nam giua 2 hinh", (0, 255, 0), inner_rect, outer_rect, center_ellipse, axes_ellipse
    else:
        return "Ngoai khoang trung tam", (0, 0, 255), inner_rect, outer_rect, center_ellipse, axes_ellipse
