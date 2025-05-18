import customtkinter as ctk
from PIL import Image, ImageTk
import os
from Service.Employee_Service import EmployeeService


class Tao_giao_dien_tai_khoan:
    def tao_giao_dien_tai_khoan(self, khung_noi_dung, id_employee):
        self.main_color = "#5CA9EB"  # Xanh đậm
        self.text_color = "#ffffff"  # Trắng
        self.accent_color = "#4a8fe7"  # Xanh nhạt
        self.bg_color = "#e9e9e9"  # Xám nhạt

        self.font_header = ("Roboto", 16, "bold")
        self.font_normal = ("Roboto", 12)
        self.font_title = ("Roboto", 14, "bold")

        self.profile_image = None
        employee = EmployeeService().get_employees_by_id_employee(id_employee)
        # Xóa các widget hiện có trong khung nội dung
        for widget in khung_noi_dung.winfo_children():
            widget.destroy()

        # Tạo khung chính
        main_frame = ctk.CTkFrame(khung_noi_dung, fg_color=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Phần tiêu đề
        header_frame = ctk.CTkFrame(main_frame, fg_color=self.main_color, corner_radius=10)
        header_frame.pack(fill="x", padx=10, pady=10)

        header_label = ctk.CTkLabel(
            header_frame,
            text="THÔNG TIN TÀI KHOẢN NHÂN VIÊN",
            font=self.font_header,
            text_color=self.text_color
        )
        header_label.pack(pady=15)

        # Tạo khung chứa ảnh và thông tin
        info_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        info_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Phần ảnh đại diện (bên trái)
        left_col = ctk.CTkFrame(info_container, fg_color="transparent")
        left_col.pack(side="left", padx=10, pady=10, fill="y")

        image_frame = ctk.CTkFrame(left_col, fg_color=self.main_color, corner_radius=10)
        image_frame.pack(padx=10, pady=10, fill="y")

        # Tải ảnh mặc định hoặc ảnh của nhân viên
        self.load_profile_image(id_employee)

        profile_label = ctk.CTkLabel(image_frame, text="", image=self.profile_image)
        profile_label.pack(padx=20, pady=20)

        # Nút Chỉnh sửa thông tin đặt dưới ảnh đại diện
        edit_btn = ctk.CTkButton(
            left_col,
            text="Chỉnh sửa thông tin",
            fg_color=self.accent_color,
            hover_color=self.main_color,
            command=lambda: self.edit_employee_info(employee)
        )
        edit_btn.pack(pady=10, padx=10, fill="x")

        # Khung chứa thông tin bên phải
        right_container = ctk.CTkFrame(info_container, fg_color="transparent")
        right_container.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Tạo hai cột cho thông tin cá nhân (+ liên hệ) và thông tin công việc
        info_row = ctk.CTkFrame(right_container, fg_color="transparent")
        info_row.pack(fill="both", expand=True, pady=5)

        # Cột thông tin cá nhân và liên hệ (bên trái của right_container)
        personal_col = ctk.CTkFrame(info_row, fg_color="transparent")
        personal_col.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Cột thông tin công việc (bên phải của right_container)
        work_col = ctk.CTkFrame(info_row, fg_color="transparent")
        work_col.pack(side="left", fill="both", expand=True, padx=(5, 0))

        # === PHẦN THÔNG TIN CÁ NHÂN VÀ LIÊN HỆ ===
        personal_title = ctk.CTkLabel(
            personal_col,
            text="THÔNG TIN CÁ NHÂN VÀ LIÊN HỆ",
            font=self.font_title,
            text_color=self.main_color,
            anchor="w"
        )
        personal_title.pack(anchor="w", padx=10, pady=(0, 10))

        # Khung thông tin cá nhân và liên hệ
        personal_frame = ctk.CTkFrame(personal_col, fg_color="#f5f5f5", corner_radius=5)
        personal_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Hiển thị từng trường thông tin cá nhân
        self.create_info_field(personal_frame, "Mã nhân viên:", employee['id_employee'])
        self.create_info_field(personal_frame, "Họ và tên:", employee['name'])
        self.create_info_field(personal_frame, "Ngày sinh:", employee['date_of_birth'])
        self.create_info_field(personal_frame, "Giới tính:", employee['gender'])
        self.create_info_field(personal_frame, "CCCD/CMND:", employee['cccd'])

        # Thêm các trường thông tin liên hệ vào cùng khung
        self.create_info_field(personal_frame, "Số điện thoại:", employee['phonenumber'])
        self.create_info_field(personal_frame, "Email:", employee['email'])
        self.create_info_field(personal_frame, "Địa chỉ:", employee['address'])

        # === PHẦN THÔNG TIN CÔNG VIỆC (bên cạnh thông tin cá nhân) ===
        work_title = ctk.CTkLabel(
            work_col,
            text="THÔNG TIN CÔNG VIỆC",
            font=self.font_title,
            text_color=self.main_color,
            anchor="w"
        )
        work_title.pack(anchor="w", padx=10, pady=(0, 10))

        # Khung thông tin công việc
        work_frame = ctk.CTkFrame(work_col, fg_color="#f5f5f5", corner_radius=5)
        work_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Hiển thị từng trường thông tin công việc
        self.create_info_field(work_frame, "Phòng ban:", employee['department'])
        self.create_info_field(work_frame, "Chức vụ:", employee['position'])
        self.create_info_field(work_frame, "Trạng thái:", employee['status'])

        # Đã di chuyển nút Chỉnh sửa thông tin xuống dưới ảnh đại diện

    def create_info_field(self, parent, label_text, value_text):
        """Tạo trường hiển thị thông tin dạng nhãn và giá trị"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=5, padx=10)

        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=self.font_normal,
            width=120,
            anchor="w"
        )
        label.pack(side="left")

        value = ctk.CTkLabel(
            frame,
            text=value_text if value_text else "Chưa cập nhật",
            font=self.font_normal,
            anchor="w"
        )
        value.pack(side="left", fill="x", expand=True)

    def load_profile_image(self, id_employee):
        """Tải ảnh đại diện hoặc sử dụng ảnh mặc định"""
        try:
            # Kiểm tra xem có ảnh cho nhân viên không (có thể điều chỉnh theo cách lưu ảnh củ bạn)
            pic_name = f"{id_employee}_001.png"
            profile_image_path = f"E:/PythonProjectMain/AI/DataSet/FaceData/processed/{id_employee}/{pic_name}"  # Thay bằng đường dẫn thực
            print(profile_image_path)
            if os.path.exists(profile_image_path):
                # Sử dụng CTkImage thay vì ImageTk.PhotoImage
                self.profile_image = ctk.CTkImage(
                    light_image=Image.open(profile_image_path),
                    dark_image=Image.open(profile_image_path),
                    size=(150, 150)
                )
            else:
                # Tạo ảnh trống nếu không tìm thấy ảnh
                blank_img = Image.new('RGB', (150, 150), color=(200, 200, 200))
                self.profile_image = ctk.CTkImage(
                    light_image=blank_img,
                    dark_image=blank_img,
                    size=(150, 150)
                )

        except Exception as e:
            print(f"Lỗi khi tải ảnh: {e}")
            # Tạo ảnh trống nếu có lỗi
            blank_img = Image.new('RGB', (150, 150), color=(200, 200, 200))
            self.profile_image = ctk.CTkImage(
                light_image=blank_img,
                dark_image=blank_img,
                size=(150, 150)
            )

    def edit_employee_info(self, employee):
        # Phương thức xử lý khi nhấn nút chỉnh sửa
        print(f"Chỉnh sửa thông tin cho nhân viên: {employee['id_employee']}")
        # Thêm code chụp ảnh ở đây

