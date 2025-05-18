from itertools import dropwhile

import customtkinter as ctk
import datetime
from View.ManagerView.GiaoDienQuanLy import Tao_giao_dien_quan_ly
from View.ManagerView.GiaoDienTrangChu import Tao_Giao_Dien_Trang_Chu
from View.ManagerView.GiaoDienMatKhau import Tao_giao_dien_mat_khau
from View.ManagerView.GiaoDienTaiKhoan import Tao_giao_dien_tai_khoan
from Service.Timekeeping_Service import TimekeepingService
from Service.Employee_Service import EmployeeService
from datetime import date

class TaoGiaoDien:
    def __init__(self, root, controller,id_enployee):
        self.id_employee=id_enployee
        self.root = root
        self.controller = controller
        self.khung_noi_dung = None

        # Set appearance mode and default color theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def tao_giao_dien(self):
        # Cấu hình khung chính
        self.root.configure(bg="#FF9966")

        # Tạo khung header
        self.tao_header()

        # Tạo thanh điều hướng bên trái
        self.tao_thanh_dieu_huong()

        # Tạo khung nội dung chính
        self.khung_noi_dung = ctk.CTkFrame(self.root, fg_color=("#5CA9EB", "#4A94D6"), corner_radius=10)
        self.khung_noi_dung.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=10, pady=10)

        # Hiển thị bảng điều khiển mặc định
        self.controller.hien_thi_trang_chu()

    def tao_header(self):
        # Khung header
        khung_header = ctk.CTkFrame(self.root, fg_color="White", corner_radius=5)
        khung_header.pack(fill=ctk.X, padx=5, pady=5)

        # Ngày giờ
        clock_icon = ctk.CTkLabel(khung_header, text="⌚", font=("Times New Roman", 40), fg_color="White")
        clock_icon.pack(side=ctk.LEFT,padx=10)

        thoi_gian_hien_tai = datetime.datetime.now().strftime("%H:%M:%S")
        ngay_hien_tai = datetime.datetime.now().strftime("%d/%m/%Y")

        khung_thoi_gian = ctk.CTkFrame(khung_header, fg_color="White", corner_radius=0)
        khung_thoi_gian.pack(side=ctk.LEFT, padx=10)

        nhan_thoi_gian = ctk.CTkLabel(khung_thoi_gian, text=thoi_gian_hien_tai,
                                      font=("Times New Roman", 16, "bold"), text_color="black", fg_color="White")
        nhan_thoi_gian.pack(anchor=ctk.W)

        nhan_ngay = ctk.CTkLabel(khung_thoi_gian, text=ngay_hien_tai,
                                 font=("Times New Roman", 16), text_color="black", fg_color="White")
        nhan_ngay.pack(anchor=ctk.W)

        # Tiêu đề
        nhan_tieu_de = ctk.CTkLabel(khung_header, text="Hệ thống nhận diện khuôn mặt",
                                    font=("Arial", 20, "bold"), text_color="black", fg_color="White")
        nhan_tieu_de.pack(side=ctk.LEFT, expand=True)

        # Cập nhật thời gian
        self.cap_nhat_thoi_gian(nhan_thoi_gian)

    def cap_nhat_thoi_gian(self, nhan_thoi_gian):
        thoi_gian_hien_tai = datetime.datetime.now().strftime("%H:%M:%S")
        nhan_thoi_gian.configure(text=thoi_gian_hien_tai)
        self.root.after(1000, lambda: self.cap_nhat_thoi_gian(nhan_thoi_gian))

    def tao_thanh_dieu_huong(self):
        sidebar_buttons = {"Trang chủ": "🏠", "Quản lý": "📋", "Thông tin\ntài khoản":"🧾", "Mật khẩu": "🔒", "Trở lại": "📤"}

        # Khung điều hướng (sidebar trái)
        khung_dieu_huong = ctk.CTkFrame(self.root, fg_color="#EEEEEE", corner_radius=10, width=90)
        khung_dieu_huong.pack(side=ctk.LEFT, fill=ctk.Y, padx=10, pady=5)
        # Các nút điều hướng
        for text, icon in sidebar_buttons.items():
            command = None
            if text == "Trang chủ":
                command = self.controller.hien_thi_trang_chu
            elif text == "Quản lý":
                command = self.controller.hien_thi_quan_ly
            elif text == "Thông tin\ntài khoản":
                command = self.controller.hien_thi_thong_tin_tai_khoan
            elif text == "Mật khẩu":
                command = self.controller.hien_thi_mat_khau
            elif text == "Trở lại":
                command = self.controller.thoat_chuong_trinh

            self.tao_nut_dieu_huong(khung_dieu_huong, text, icon, command)
    def tao_nut_dieu_huong(self, parent, text, icon, command):
        button_text = f"{icon}\n{text}"
        nut = ctk.CTkButton(parent, text=button_text, font=("Arial", 16),
                            fg_color="White", hover_color="#DDDDDD", border_width=2,
                            border_color="black", text_color="black", command=command,corner_radius=15,
                            width=100, height=80)
        nut.pack(pady=10, padx=10)
        nut.pack_propagate(False)

    def tao_trang_chu(self):
        employee = EmployeeService()
        timekeeping = TimekeepingService()
        so_nhan_vien = len(employee.get_all_employees())
        so_nguoi_diem_danh = len(timekeeping.get_timekeeping_by_date(f"{date.today()}"))
        so_nguoi_dang_lam = len(employee.count_employees_dang_lam())
        for widget in self.khung_noi_dung.winfo_children():
            widget.destroy()
        self.giao_dien=Tao_Giao_Dien_Trang_Chu()
        self.giao_dien.tao_giao_dien_trang_chu(self.khung_noi_dung,so_nhan_vien,so_nguoi_diem_danh,so_nguoi_dang_lam)

    def tao_giao_dien_quan_ly(self):
        for widget in self.khung_noi_dung.winfo_children():
            widget.destroy()
        self.giao_dien=Tao_giao_dien_quan_ly()
        self.giao_dien.tao_giao_dien_quan_ly(self.khung_noi_dung)

    def tao_giao_dien_mat_khau(self):
        for widget in self.khung_noi_dung.winfo_children():
            widget.destroy()
        self.giao_dien=Tao_giao_dien_mat_khau()
        self.giao_dien.tao_giao_dien_mat_khau(self.khung_noi_dung,self.id_employee)

    def tao_giao_dien_tai_khoan(self):
        for widget in self.khung_noi_dung.winfo_children():
            widget.destroy()
        self.giao_dien= Tao_giao_dien_tai_khoan()
        self.giao_dien.tao_giao_dien_tai_khoan(self.khung_noi_dung,self.id_employee)