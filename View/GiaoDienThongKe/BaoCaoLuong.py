import customtkinter as ctk
from datetime import datetime
from tkinter import ttk
import locale


class SalaryPage:
    def __init__(self, parent, employees, salarys):
        self.parent = parent
        self.employees = employees
        self.salarys = salarys


        # Frame chính
        self.main_frame = ctk.CTkFrame(parent)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Frame điều khiển
        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.control_frame.pack(fill="x", padx=10, pady=10)

        # Label tiêu đề
        self.title_label = ctk.CTkLabel(
            self.control_frame,
            text="BÁO CÁO LƯƠNG NHÂN VIÊN",
            font=("Arial", 20, "bold")
        )
        self.title_label.pack(pady=10)

        # Frame lọc theo phòng ban
        self.filter_frame = ctk.CTkFrame(self.control_frame)
        self.filter_frame.pack(fill="x", padx=10, pady=10)

        # Label và Combobox cho phòng ban
        ctk.CTkLabel(self.filter_frame, text="Phòng ban:",font=("Arial", 16)).pack(side="left", padx=5)

        # Lấy danh sách các phòng ban từ dữ liệu nhân viên
        departments = ["Tất cả"] + list(set(emp[6].strip() for emp in self.employees))

        self.department_var = ctk.StringVar(value="Tất cả")
        self.department_combobox = ctk.CTkComboBox(
            self.filter_frame,
            values=departments,
            variable=self.department_var,
            width=150
        )
        self.department_combobox.pack(side="left", padx=5)

        # Nút tìm kiếm
        self.search_btn = ctk.CTkButton(
            self.filter_frame,
            text="Tìm kiếm",font=("Arial", 16),
            command=self.search_salary
        )
        self.search_btn.pack(side="left", padx=20)

        # Frame kết quả
        self.result_frame = ctk.CTkFrame(self.main_frame)
        self.result_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Tạo Treeview cho dữ liệu lương
        self.create_treeview()

        # Hiển thị dữ liệu mặc định
        self.search_salary()

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
        style.configure("Treeview.Heading", font=('Arial', 14, 'bold'))

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("id", "name", "department", "position", "basic_salary", "allowance", "total_salary"),
            show="headings",
            yscrollcommand=self.tree_scroll.set
        )

        # Thiết lập các cột
        self.tree.heading("id", text="ID Nhân viên")
        self.tree.heading("name", text="Tên nhân viên")
        self.tree.heading("department", text="Phòng ban")
        self.tree.heading("position", text="Vị trí")
        self.tree.heading("basic_salary", text="Lương cơ bản")
        self.tree.heading("allowance", text="Phụ cấp")
        self.tree.heading("total_salary", text="Tổng lương")

        # Định dạng độ rộng các cột
        self.tree.column("id", width=100, anchor="center")
        self.tree.column("name", width=200)
        self.tree.column("department", width=100)
        self.tree.column("position", width=100)
        self.tree.column("basic_salary", width=150, anchor="e")
        self.tree.column("allowance", width=150, anchor="e")
        self.tree.column("total_salary", width=150, anchor="e")

        # Đặt màu sắc xen kẽ cho các dòng
        self.tree.tag_configure('oddrow', background='#EEEEEE')
        self.tree.tag_configure('evenrow', background='#FFFFFF')

        self.tree.pack(expand=True, fill="both")
        self.tree_scroll.configure(command=self.tree.yview)

        # Label hiển thị tổng lương
        self.total_salary_label = ctk.CTkLabel(
            self.result_frame,
            text="Tổng lương của phòng ban: 0 VNĐ",
            anchor="w",
            font=("Arial", 16, "bold")
        )
        self.total_salary_label.pack(anchor="w", padx=10, pady=5)

        # Label hiển thị số lượng kết quả
        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="Số lượng nhân viên: 0",
            anchor="w",font=("Arial", 16)
        )
        self.result_label.pack(anchor="w", padx=10, pady=5)

    def search_salary(self):
        # Xóa dữ liệu cũ trong treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Lấy phòng ban đã chọn
        department = self.department_var.get()

        # Lọc nhân viên theo phòng ban
        if department == "Tất cả":
            filtered_employees = self.employees
        else:
            filtered_employees = [emp for emp in self.employees if emp[6] == department]

        # Tạo dictionary ánh xạ id_employee với thông tin lương
        salary_dict = {sal[4]: sal for sal in self.salarys}

        count = 0
        total_salary = 0

        for idx, emp in enumerate(filtered_employees):
            id_employee = emp[0]
            if id_employee in salary_dict:
                sal = salary_dict[id_employee]

                # Format tiền tệ theo định dạng Việt Nam
                basic_salary = f"{int(sal[1]):,} VNĐ".replace(",", ".")
                allowance = f"{int(sal[2]):,} VNĐ".replace(",", ".")
                total = f"{int(sal[3]):,} VNĐ".replace(",", ".")

                values = (
                    id_employee,  # ID nhân viên
                    emp[1],  # Tên
                    emp[6],  # Phòng ban
                    emp[8],  # Vị trí
                    basic_salary,  # Lương cơ bản
                    allowance,  # Phụ cấp
                    total  # Tổng lương
                )
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert('', 'end', values=values, tags=(tag,))
                count += 1
                total_salary += int(sal[3])

        # Cập nhật label tổng lương
        formatted_total = f"{total_salary:,} VNĐ".replace(",", ".")
        self.total_salary_label.configure(text=f"Tổng lương của phòng ban: {formatted_total}")

        # Cập nhật label số lượng nhân viên
        self.result_label.configure(text=f"Số lượng nhân viên: {count}")

    def get_table_data(self):
        headers = [
            "ID Nhân viên",
            "Tên nhân viên",
            "Phòng ban",
            "Vị trí",
            "Lương cơ bản",
            "Phụ cấp",
            "Tổng lương"
        ]
        data = []
        for item in self.tree.get_children():
            row_data = self.tree.item(item)['values']
            # Đảm bảo dữ liệu không có None và giữ nguyên định dạng tiền tệ
            row_data = [str(val) if val is not None else "0 VNĐ" for val in row_data]
            data.append(row_data)
        return headers, data