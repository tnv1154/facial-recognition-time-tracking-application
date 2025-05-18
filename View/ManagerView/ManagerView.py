import customtkinter as ctk
from tkinter import messagebox

from View.ManagerView.GiaoDienChinh import TaoGiaoDien

class Tao_Giao_Dien_Chinh:
    def __init__(self,rootapp, root,id_employee):
        self.rootapp=rootapp
        # Các đối tượng quản lý
        self.root=root
        # Tạo giao diện
        self.root.title("Hệ thống quản lý chấm công nhân viên")
        self.root.geometry("1000x600")
        self.root.configure(bg="#FF9966")
        # Khởi tạo dữ liệu mẫu

        self.giao_dien = TaoGiaoDien(self.root, self,id_employee)
        self.giao_dien.tao_giao_dien()

    def hien_thi_trang_chu(self):
        self.giao_dien.tao_trang_chu()

    def hien_thi_quan_ly(self):
        self.giao_dien.tao_giao_dien_quan_ly()

    def hien_thi_thong_tin_tai_khoan(self):
        self.giao_dien.tao_giao_dien_tai_khoan()

    def hien_thi_mat_khau(self):
        self.giao_dien.tao_giao_dien_mat_khau()

    def thoat_chuong_trinh(self):
        if messagebox.askokcancel("Thoát", "Bạn có chắc muốn thoát chương trình?"):
            self.root.destroy()
            self.rootapp.deiconify()
    def xuat_excel(self):
        messagebox.showinfo("Xuất Excel", "Đã xuất dữ liệu ra file Excel thành công!")

if __name__ == "__main__":
    root = ctk.CTk()
    app = Tao_Giao_Dien_Chinh(root,root,3)
    root.mainloop()
