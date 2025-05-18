import customtkinter as ctk
import os
from PIL import Image
from tkinter import messagebox
from PIL.ImageOps import expand
from Service.Account_Service import AccountService

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class Tao_giao_dien_mat_khau(ctk.CTk):
    def tao_giao_dien_mat_khau(self,khung_noi_dung,id_employee):

        # Thiết lập nền gradient
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.khung_noi_dung=khung_noi_dung
        account=AccountService().get_account_by_id(id_employee)
        # Tạo khung chính
        self.khung_chinh = ctk.CTkFrame(self.khung_noi_dung, corner_radius=10, fg_color="white")
        self.khung_chinh.grid(row=0, column=0, padx=240, pady=30)

        # Nhãn tiêu đề
        self.nhan_tieu_de = ctk.CTkLabel(self.khung_chinh, text="Đổi mật khẩu",
                                         font=ctk.CTkFont(size=20, weight="bold"))
        self.nhan_tieu_de.grid(row=0, column=0, padx=30, pady=(20, 20))

        # Trường nhập tài khoản
        self.nhan_tai_khoan = ctk.CTkLabel(self.khung_chinh, text="Tài khoản", anchor="w")
        self.nhan_tai_khoan.grid(row=1, column=0, padx=30, pady=(10, 0), sticky="w")

        self.nhap_tai_khoan = ctk.CTkEntry(self.khung_chinh, width=300)
        self.nhap_tai_khoan.grid(row=2, column=0, padx=30, pady=(0, 10))
        self.nhap_tai_khoan.insert(0, account["username"])
        self.nhap_tai_khoan.configure(state="disabled")
        # Trường nhập mật khẩu cũ
        self.nhan_mat_khau_cu = ctk.CTkLabel(self.khung_chinh, text="Mật khẩu cũ", anchor="w")
        self.nhan_mat_khau_cu.grid(row=3, column=0, padx=30, pady=(10, 0), sticky="w")

        self.nhap_mat_khau_cu = ctk.CTkEntry(self.khung_chinh, width=300, show="*")
        self.nhap_mat_khau_cu.grid(row=4, column=0, padx=30, pady=(0, 10))

        # Trường nhập mật khẩu mới
        self.nhan_mat_khau_moi = ctk.CTkLabel(self.khung_chinh, text="Mật khẩu mới", anchor="w")
        self.nhan_mat_khau_moi.grid(row=5, column=0, padx=30, pady=(10, 0), sticky="w")

        self.nhap_mat_khau_moi = ctk.CTkEntry(self.khung_chinh, width=300, show="*")
        self.nhap_mat_khau_moi.grid(row=6, column=0, padx=30, pady=(0, 10))

        # Trường nhập lại mật khẩu mới
        self.nhan_nhap_lai_mat_khau = ctk.CTkLabel(self.khung_chinh, text="Nhập lại mật khẩu", anchor="w")
        self.nhan_nhap_lai_mat_khau.grid(row=7, column=0, padx=30, pady=(10, 0), sticky="w")

        self.nhap_lai_mat_khau = ctk.CTkEntry(self.khung_chinh, width=300, show="*")
        self.nhap_lai_mat_khau.grid(row=8, column=0, padx=30, pady=(0, 10))

        # Nút xác nhận
        self.nut_xac_nhan = ctk.CTkButton(
            self.khung_chinh,
            text="Xác nhận",
            corner_radius=5,
            fg_color="#ff9d40",
            hover_color="#ff7e5f",
            command=lambda: self.gui_bieu_mau(account)
        )
        self.nut_xac_nhan.grid(row=9, column=0, padx=30, pady=(20, 20))

    def gui_bieu_mau(self,account):
        tai_khoan = self.nhap_tai_khoan.get()
        mat_khau_cu = self.nhap_mat_khau_cu.get()
        mat_khau_moi = self.nhap_mat_khau_moi.get()
        xac_nhan_mat_khau = self.nhap_lai_mat_khau.get()

        # Kiểm tra dữ liệu nhập vào
        if not all([tai_khoan, mat_khau_cu, mat_khau_moi, xac_nhan_mat_khau]):
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
            return

        if mat_khau_moi != xac_nhan_mat_khau:
            messagebox.showerror("Lỗi", "Mật khẩu mới không khớp với mật khẩu xác nhận!")
            return

        if len(mat_khau_moi) < 6:
            messagebox.showwarning("Cảnh báo", "Mật khẩu mới phải có ít nhất 6 ký tự!")
            return

        if mat_khau_cu != account["password"]:
            messagebox.showerror("Lỗi", "Mật khẩu cũ không đúng!")
            return
        AccountService().update_password(account["username"],mat_khau_moi)
        messagebox.showinfo("Thành công", f"Đổi mật khẩu thành công cho tài khoản: {tai_khoan}")

        self.nhap_mat_khau_cu.delete(0, 'end')
        self.nhap_mat_khau_moi.delete(0, 'end')
        self.nhap_lai_mat_khau.delete(0, 'end')
