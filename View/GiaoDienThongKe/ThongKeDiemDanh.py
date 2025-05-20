import customtkinter as ctk
from datetime import datetime
import calendar
import locale
from tkinter import ttk
from datetime import datetime, timedelta
from Service.Employee_Service import EmployeeService
from Service.Timekeeping_Service import TimekeepingService
from Service.Salary_Service import SalaryService
from Models.Employee import Employee
from Models.Timekeeping import Timekeeping
from Models.Salary import Salary

class AttendancePage:
    def __init__(self, parent):
        emp = EmployeeService().get_all_employees()
        employees = [[str(value) for value in d.values()] for d in emp]

        timek = TimekeepingService().get_all_timekeeping()
        timekeepings = [[str(value) for value in d.values()] for d in timek]

        self.parent = parent
        self.employees = employees
        self.timekeepings = timekeepings

        self.current_date = datetime.now()

        self.main_frame = ctk.CTkFrame(parent)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Frame điều khiển
        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.control_frame.pack(fill="x", padx=10, pady=10)

        # Label tiêu đề
        self.title_label = ctk.CTkLabel(
            self.control_frame,
            text="THỐNG KÊ ĐIỂM DANH THEO NGÀY",
            font=("Arial", 20, "bold")
        )
        self.title_label.pack(pady=10)

        self.date_frame = ctk.CTkFrame(self.control_frame)
        self.date_frame.pack(fill="x", padx=10, pady=10)

        # Label và Combobox cho ngày
        ctk.CTkLabel(self.date_frame, text="Ngày:",font=("Arial", 16)).grid(row=0, column=0, padx=5, pady=5)
        self.day_var = ctk.StringVar(value=str(self.current_date.day))
        self.day_combobox = ctk.CTkComboBox(
            self.date_frame,
            values=[str(i) for i in range(1, 32)],
            variable=self.day_var,
            width=70
        )
        self.day_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Label và Combobox cho tháng
        ctk.CTkLabel(self.date_frame, text="Tháng:",font=("Arial", 16)).grid(row=0, column=2, padx=5, pady=5)
        self.month_var = ctk.StringVar(value=str(self.current_date.month))
        self.month_combobox = ctk.CTkComboBox(
            self.date_frame,
            values=[str(i) for i in range(1, 13)],
            variable=self.month_var,
            width=70
        )
        self.month_combobox.grid(row=0, column=3, padx=5, pady=5)

        # Label và Combobox cho năm
        ctk.CTkLabel(self.date_frame, text="Năm:",font=("Arial", 16)).grid(row=0, column=4, padx=5, pady=5)
        self.year_var = ctk.StringVar(value=str(self.current_date.year))
        self.year_combobox = ctk.CTkComboBox(
            self.date_frame,
            values=[str(i) for i in range(self.current_date.year - 5, self.current_date.year + 1)],
            variable=self.year_var,
            width=90
        )
        self.year_combobox.grid(row=0, column=5, padx=5, pady=5)

        self.search_btn = ctk.CTkButton(
            self.date_frame,
            text="Tìm kiếm",font=("Arial", 16),
            command=self.search_attendance
        )
        self.search_btn.grid(row=0, column=6, padx=20, pady=5)

        self.result_frame = ctk.CTkFrame(self.main_frame)
        self.result_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.create_treeview()
        self.search_attendance()

    def create_treeview(self):
        # Tạo frame cho Treeview
        self.tree_frame = ctk.CTkFrame(self.result_frame)
        self.tree_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Tạo Scrollbar
        self.tree_scroll = ctk.CTkScrollbar(self.tree_frame)
        self.tree_scroll.pack(side="right", fill="y")

        style = ttk.Style()
        style.theme_use('default')

        # Cấu hình font với kích thước lớn hơn
        style.configure("Treeview", font=('Arial', 14), rowheight=35)
        style.configure("Treeview.Heading", font=('Arial', 14, 'bold'))

        # Áp dụng cấu hình cho tất cả các thành phần của Treeview
        style.map('Treeview', font=[('', ('Arial', 14))])

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("id", "name", "department", "position", "check_in", "check_out"),
            show="headings",
            yscrollcommand=self.tree_scroll.set
        )

        # Thiết lập các cột
        self.tree.heading("id", text="ID Nhân viên")
        self.tree.heading("name", text="Tên nhân viên")
        self.tree.heading("department", text="Phòng ban")
        self.tree.heading("position", text="Vị trí")
        self.tree.heading("check_in", text="Giờ check-in")
        self.tree.heading("check_out", text="Giờ check-out")

        # Định dạng độ rộng các cột
        self.tree.column("id", width=100, anchor="center")
        self.tree.column("name", width=200)
        self.tree.column("department", width=150)
        self.tree.column("position", width=150)
        self.tree.column("check_in", width=100, anchor="center")
        self.tree.column("check_out", width=100, anchor="center")

        # Đặt màu sắc xen kẽ cho các dòng
        self.tree.tag_configure('oddrow', background='#EEEEEE')
        self.tree.tag_configure('evenrow', background='#FFFFFF')

        self.tree.pack(expand=True, fill="both")
        self.tree_scroll.configure(command=self.tree.yview)

        # Label hiển thị số lượng kết quả
        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="Số lượng nhân viên: 0",
            anchor="w",font=("Arial", 16)
        )
        self.result_label.pack(anchor="w", padx=10, pady=5)

    def search_attendance(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Lấy ngày tháng từ combobox
        try:
            day = int(self.day_var.get())
            month = int(self.month_var.get())
            year = int(self.year_var.get())

            # Kiểm tra ngày hợp lệ
            days_in_month = calendar.monthrange(year, month)[1]
            if day > days_in_month:
                day = days_in_month
                self.day_var.set(str(day))

            selected_date = f"{year}-{month:02d}-{day:02d}"
        except ValueError:
            selected_date = datetime.now().strftime("%Y-%m-%d")

        # Lọc dữ liệu timekeeping theo ngày
        filtered_timekeepings = [tk for tk in self.timekeepings if tk[3] == selected_date]
        # Tạo dictionary để ánh xạ id_employee với thông tin nhân viên
        employee_dict = {emp[0]: emp for emp in self.employees}

        count = 0
        for idx, tk in enumerate(filtered_timekeepings):
            id_employee = tk[2]
            if id_employee in employee_dict:
                emp = employee_dict[id_employee]
                values = (
                    id_employee,  # ID nhân viên
                    emp[1],  # Tên
                    emp[6],  # Phòng ban
                    emp[8],  # Vị trí
                    tk[1],  # Giờ check-in
                    tk[4]  # Giờ check-out
                )
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert('', 'end', values=values, tags=(tag,))
                count += 1

        self.result_label.configure(text=f"Số lượng nhân viên: {count}")

    def get_table_data(self):
        headers = [
            "ID Nhân viên",
            "Tên nhân viên",
            "Phòng ban",
            "Vị trí",
            "Giờ check-in",
            "Giờ check-out"
        ]
        data = []
        for item in self.tree.get_children():
            row_data = self.tree.item(item)['values']
            # Đảm bảo dữ liệu không có None
            row_data = [str(val) if val is not None else "" for val in row_data]
            data.append(row_data)
        return headers, data
