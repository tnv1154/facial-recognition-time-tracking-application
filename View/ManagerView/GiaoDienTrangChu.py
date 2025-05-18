import customtkinter as ctk

class Tao_Giao_Dien_Trang_Chu:
    def tao_giao_dien_trang_chu(self,khung_noi_dung,so_nhan_vien,so_nguoi_diem_danh,so_nguoi_dang_lam):
        # Hàng 1
        hang_1 = ctk.CTkFrame(khung_noi_dung,fg_color=("#5CA9EB", "#4A94D6"), corner_radius=0)
        hang_1.pack(fill=ctk.X, expand=True, pady=10)

        # Ô Số nhân viên
        o_hoc_sinh = ctk.CTkFrame(hang_1, fg_color="white", width=300, height=150, corner_radius=10)
        o_hoc_sinh.pack(side=ctk.LEFT, expand=True, padx=10)
        o_hoc_sinh.pack_propagate(False)

        ctk.CTkLabel(o_hoc_sinh, text="Tổng", font=("Arial", 30, "bold"), text_color="black").pack(pady=(20, 0))
        ctk.CTkLabel(o_hoc_sinh, text=f"{so_nhan_vien}", font=("Arial", 40, "bold"), text_color="black").pack()
        ctk.CTkLabel(o_hoc_sinh, text="Nhân Viên", font=("Arial", 30, "bold"), text_color="black").pack()

        # Ô số người đang làm
        o_giao_vien = ctk.CTkFrame(hang_1, fg_color="white", width=300, height=150, corner_radius=10)
        o_giao_vien.pack(side=ctk.RIGHT, expand=True, padx=10)
        o_giao_vien.pack_propagate(False)

        ctk.CTkLabel(o_giao_vien, text="Tổng", font=("Arial", 30, "bold"), text_color="black").pack(pady=(20, 0))
        ctk.CTkLabel(o_giao_vien, text=f"{so_nguoi_dang_lam}", font=("Arial", 40, "bold"), text_color="black").pack()
        ctk.CTkLabel(o_giao_vien, text="Đang Làm", font=("Arial", 30, "bold"), text_color="black").pack()

        # Hàng 2
        hang_2 = ctk.CTkFrame(khung_noi_dung,fg_color=("#5CA9EB", "#4A94D6"), corner_radius=0)
        hang_2.pack(fill=ctk.X, expand=True, pady=10)

        # Ô số người điểm danh
        o_lop_hoc = ctk.CTkFrame(hang_2, fg_color="white", width=300, height=150, corner_radius=10)
        o_lop_hoc.pack(pady=10)  # Không dùng side=LEFT
        o_lop_hoc.pack_propagate(False)

        ctk.CTkLabel(o_lop_hoc, text="Tổng", font=("Arial", 30, "bold"), text_color="black").pack(pady=(20, 0))
        ctk.CTkLabel(o_lop_hoc, text=f'{so_nguoi_diem_danh}',font=("Arial", 30, "bold"), text_color="black").pack()
        ctk.CTkLabel(o_lop_hoc, text="Đã Điểm Danh", font=("Arial", 30, "bold"), text_color="black").pack()
