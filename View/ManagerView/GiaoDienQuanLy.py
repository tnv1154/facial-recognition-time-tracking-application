import customtkinter as ctk
from View.GiaoDienQuanLyNhanVien.QuanLyNhanVien import EmployeeManagementApp
from View.GiaoDienThongKe.GiaoDienThongKe import Giao_Dien_Thong_Ke

class Tao_giao_dien_quan_ly:
    def tao_giao_dien_quan_ly(self,khung_noi_dung ):
        # Tạo bố cục lưới 2x2 cho 4 nút
        khung_noi_dung.grid_columnconfigure(0, weight=1)
        khung_noi_dung.grid_rowconfigure(0, weight=1)

        # Định nghĩa các nút

        self.tao_nut_lon(khung_noi_dung,"👤", "Nhân Viên", 0, 0, "white", "black","Nhân Viên")
        self.tao_nut_lon(khung_noi_dung,"📅", "Thống Kê", 0, 1, "white", "black","Thống Kê")

    def tao_nut_lon(self,khung_noi_dung, icon, ten, hang, cot, mau, mau_chu,action):
        # Tạo văn bản với icon lớn và tên
        text = f"{icon}\n"

        # Tạo font tùy chỉnh với icon lớn
        custom_font = ctk.CTkFont(family="TkDefaultFont", size=50)

        # Tạo nút với kích thước lớn
        nut = ctk.CTkButton(
            khung_noi_dung,
            text=text,
            font=custom_font,
            text_color=mau_chu,
            fg_color=mau,
            hover_color=self.tao_mau_hover(mau),
            corner_radius=30,
            width=90,
            height=90,
            command=lambda : self.xu_ly_click(action),
            compound="top",
        )
        nut.grid(row=hang, column=cot, padx=148, pady=200, sticky="nsew")

        # Tạo nhãn tên riêng và đặt nó lên nút
        ten_label = ctk.CTkLabel(
            nut,
            text=ten,
            font=("TkDefaultFont", 16, "bold"),
            text_color=mau_chu
        )
        ten_label.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)

    def tao_mau_hover(self, mau_nen):
        # Tạo màu hover tối hơn một chút so với màu nền
        return "#f0f0f0"

    def xu_ly_click(self,action):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        windows=ctk.CTkToplevel()
        windows.focus_force()
        windows.lift()
        windows.attributes("-topmost", True)
        windows.after(10, lambda: windows.attributes("-topmost", False))

        if action=="Nhân Viên":
            EmployeeManagementApp(windows)
        else:
            Giao_Dien_Thong_Ke(windows)



