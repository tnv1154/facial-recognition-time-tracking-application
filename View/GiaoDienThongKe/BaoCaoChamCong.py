import customtkinter as ctk
from datetime import datetime, timedelta
from tkinter import ttk
import calendar
import locale
from datetime import datetime
from datetime import datetime, timedelta
from Service.Employee_Service import EmployeeService
from Service.Timekeeping_Service import TimekeepingService
from Service.Salary_Service import SalaryService
from Models.Employee import Employee
from Models.Timekeeping import Timekeeping
from Models.Salary import Salary

class TimesheetPage:
    def __init__(self, parent, ):
        self.parent = parent
        emp = EmployeeService().get_all_employees()
        employees = [[str(value) for value in d.values()] for d in emp]

        timek = TimekeepingService().get_all_timekeeping()
        timekeepings = [[str(value) for value in d.values()] for d in timek]

        self.employees = employees
        self.timekeepings = timekeepings

        # Lấy thời gian hiện tại
        self.current_date = datetime.now()

        # Frame chính
        self.main_frame = ctk.CTkFrame(parent)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Frame điều khiển
        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.control_frame.pack(fill="x", padx=10, pady=10)

        # Label tiêu đề
        self.title_label = ctk.CTkLabel(
            self.control_frame,
            text="BÁO CÁO CHẤM CÔNG CHI TIẾT",
            font=("Arial", 20, "bold")
        )
        self.title_label.pack(pady=10)

        # Frame chọn nhân viên và tháng
        self.filter_frame = ctk.CTkFrame(self.control_frame)
        self.filter_frame.pack(fill="x", padx=10, pady=10)

        # Label và Combobox cho nhân viên
        ctk.CTkLabel(self.filter_frame, text="ID Nhân viên:",font=("Arial", 16)).grid(row=0, column=0, padx=5, pady=5)

        # Tạo danh sách các ID nhân viên
        employee_ids = ["Tất cả"] + [emp[0] for emp in self.employees]

        self.employee_var = ctk.StringVar(value="Tất cả")
        self.employee_combobox = ctk.CTkComboBox(
            self.filter_frame,
            values=employee_ids,
            variable=self.employee_var,
            width=120
        )
        self.employee_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Label và Combobox cho tháng
        ctk.CTkLabel(self.filter_frame, text="Tháng:",font=("Arial", 16)).grid(row=0, column=2, padx=5, pady=5)
        self.month_var = ctk.StringVar(value=str(self.current_date.month))
        self.month_combobox = ctk.CTkComboBox(
            self.filter_frame,
            values=[str(i) for i in range(1, 13)],
            variable=self.month_var,
            width=70
        )
        self.month_combobox.grid(row=0, column=3, padx=5, pady=5)

        # Label và Combobox cho năm
        ctk.CTkLabel(self.filter_frame, text="Năm:",font=("Arial", 16)).grid(row=0, column=4, padx=5, pady=5)
        self.year_var = ctk.StringVar(value=str(self.current_date.year))
        self.year_combobox = ctk.CTkComboBox(
            self.filter_frame,
            values=[str(i) for i in range(self.current_date.year - 5, self.current_date.year + 1)],
            variable=self.year_var,
            width=90
        )
        self.year_combobox.grid(row=0, column=5, padx=5, pady=5)

        # Nút tìm kiếm
        self.search_btn = ctk.CTkButton(
            self.filter_frame,
            text="Tìm kiếm",font=("Arial", 16),
            command=self.search_timesheet
        )
        self.search_btn.grid(row=0, column=6, padx=20, pady=5)

        # Frame kết quả
        self.result_frame = ctk.CTkFrame(self.main_frame)
        self.result_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Tạo Treeview cho dữ liệu chấm công
        self.create_treeview()

        # Hiển thị dữ liệu mặc định
        self.search_timesheet()

    def create_treeview(self):
        # Tạo frame cho Treeview
        self.tree_frame = ctk.CTkFrame(self.result_frame)
        self.tree_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Tạo Scrollbar
        self.tree_scroll = ctk.CTkScrollbar(self.tree_frame)
        self.tree_scroll.pack(side="right", fill="y")

        # Tạo Treeview
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 14), rowheight=25)
        style.configure("Treeview.Heading", font=('Arial',14 , 'bold'))

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("id", "name", "department", "position", "total_days", "late_count", "early_leave", "total_hours"),
            show="headings",
            yscrollcommand=self.tree_scroll.set
        )

        # Thiết lập các cột
        self.tree.heading("id", text="ID Nhân viên")
        self.tree.heading("name", text="Tên nhân viên")
        self.tree.heading("department", text="Phòng ban")
        self.tree.heading("position", text="Vị trí")
        self.tree.heading("total_days", text="Tổng ngày làm")
        self.tree.heading("late_count", text="Số lần đi muộn")
        self.tree.heading("early_leave", text="Số lần về sớm")
        self.tree.heading("total_hours", text="Tổng giờ làm")

        # Định dạng độ rộng các cột
        self.tree.column("id", width=100, anchor="center")
        self.tree.column("name", width=200)
        self.tree.column("department", width=100)
        self.tree.column("position", width=100)
        self.tree.column("total_days", width=100, anchor="center")
        self.tree.column("late_count", width=100, anchor="center")
        self.tree.column("early_leave", width=100, anchor="center")
        self.tree.column("total_hours", width=100, anchor="center")

        # Đặt màu sắc xen kẽ cho các dòng
        self.tree.tag_configure('oddrow', background='#EEEEEE')
        self.tree.tag_configure('evenrow', background='#FFFFFF')

        self.tree.pack(expand=True, fill="both")
        self.tree_scroll.configure(command=self.tree.yview)

        # Label hiển thị số lượng kết quả
        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="Số lượng kết quả: 0",
            anchor="w",font=("Arial", 16)
        )
        self.result_label.pack(anchor="w", padx=10, pady=5)

    def search_timesheet(self):
        # Xóa dữ liệu cũ trong treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            month = int(self.month_var.get())
            year = int(self.year_var.get())
            employee_id = self.employee_var.get()
        except ValueError:
            month = self.current_date.month
            year = self.current_date.year
            employee_id = "Tất cả"
        # Tạo danh sách nhân viên cần hiển thị
        if employee_id == "Tất cả":
            selected_employees = self.employees
        else:
            selected_employees = [emp for emp in self.employees if emp[0] == employee_id]

        # Lọc dữ liệu timekeeping theo tháng, năm
        month_prefix = f"{month:02d}-{year}"
        filtered_timekeepings = [tk for tk in self.timekeepings if
                                 tk[3].startswith(f"{year}-") and tk[3].split("-")[1] == f"{month:02d}"]

        # Tạo dictionary để lưu thông tin chấm công theo id nhân viên
        timesheet_data = {}

        for tk in filtered_timekeepings:
            id_employee = tk[2]
            if id_employee not in timesheet_data:
                timesheet_data[id_employee] = {
                    "total_days": 0,
                    "late_count": 0,
                    "early_leave": 0,
                    "total_hours": 0
                }

            # Tăng số ngày làm việc
            timesheet_data[id_employee]["total_days"] += 1

            # Kiểm tra đi muộn (sau 8:00)
            check_in_hour, check_in_minute = map(int, tk[1].split(":"))
            if check_in_hour > 8 or (check_in_hour == 8 and check_in_minute > 0):
                timesheet_data[id_employee]["late_count"] += 1

            # Kiểm tra về sớm (trước 17:00)
            if len(tk[4]) == 5:
                check_out_hour, check_out_minute = map(int, tk[4].split(":"))
                if check_out_hour < 17:
                    timesheet_data[id_employee]["early_leave"] += 1

                # Tính tổng giờ làm việc
                total_hours = (check_out_hour * 60 + check_out_minute - (check_in_hour * 60 + check_in_minute)) / 60
                timesheet_data[id_employee]["total_hours"] += total_hours

        count = 0
        for idx, emp in enumerate(selected_employees):
            id_employee = emp[0]
            if id_employee in timesheet_data:
                data = timesheet_data[id_employee]
                values = (
                    id_employee,  # ID nhân viên
                    emp[1],  # Tên
                    emp[6],  # Phòng ban
                    emp[8],  # Vị trí
                    data["total_days"],  # Tổng ngày làm
                    data["late_count"],  # Số lần đi muộn
                    data["early_leave"],  # Số lần về sớm
                    f"{data['total_hours']:.2f}"  # Tổng giờ làm
                )
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert('', 'end', values=values, tags=(tag,))
                count += 1

        # Cập nhật label số lượng
        self.result_label.configure(text=f"Số lượng kết quả: {count}")

    def get_table_data(self):
        headers = [
            "ID Nhân viên",
            "Tên nhân viên",
            "Phòng ban",
            "Vị trí",
            "Tổng ngày làm",
            "Số lần đi muộn",
            "Số lần về sớm",
            "Tổng giờ làm"
        ]
        data = []
        for item in self.tree.get_children():
            row_data = self.tree.item(item)['values']
            # Đảm bảo dữ liệu không có None và định dạng số
            row_data = [
                str(val) if val is not None else ""
                if i != 7  # Giữ nguyên định dạng số cho cột tổng giờ làm
                else f"{float(val):.2f}" if val is not None else "0.00"
                for i, val in enumerate(row_data)
            ]
            data.append(row_data)
        return headers, data