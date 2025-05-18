import customtkinter as ctk
from View.GiaoDienQuanLyNhanVien.ThongTinNhanVien import EmployeeInfoFrame
from View.GiaoDienQuanLyNhanVien.TimKiemNhanVien import SearchFrame
from View.GiaoDienQuanLyNhanVien.DatabaseService import DatabaseManager


class EmployeeManagementApp(ctk.CTk):
    def __init__(self,parents):
        # Kết nối database
        self.db_manager = DatabaseManager()
        self.parents=parents
        # Thiết lập cửa sổ
        self.parents.title("Quản lý Nhân viên")
        self.parents.geometry("1200x700")

        # Tạo tiêu đề
        self.header_label = ctk.CTkLabel(self.parents, text="Quản lý Nhân viên",
                                         font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.pack(pady=20)

        # Tạo khung chính
        self.main_frame = ctk.CTkFrame(self.parents)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Chia làm 2 phần
        self.left_frame = ctk.CTkFrame(self.main_frame)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.right_frame = ctk.CTkFrame(self.main_frame)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Thêm frame thông tin nhân viên
        self.employee_info_frame = EmployeeInfoFrame(self.left_frame, self.db_manager)
        self.employee_info_frame.pack(fill="both", expand=True)

        # Thêm frame tìm kiếm
        self.search_frame = SearchFrame(self.right_frame, self.db_manager)
        self.search_frame.pack(fill="both", expand=True)

        # Liên kết các sự kiện
        self.search_frame.set_edit_callback(self.employee_info_frame.load_employee_data)