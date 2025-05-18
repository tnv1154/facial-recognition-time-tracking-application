import customtkinter as ctk
class SearchFrame(ctk.CTkFrame):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db_manager = db_manager
        self.edit_callback = None
        self.selected_row = None  # Theo dõi hàng đang được chọn
        self.row_frames = []  # Danh sách các khung hàng

        # Màu sắc
        self.default_row_color = "transparent"  # Màu mặc định cho hàng
        self.selected_row_color = "#3498db"  # Màu khi hàng được chọn

        # Tạo nội dung
        self.setup_ui()
        self.load_employee_data()

    def setup_ui(self):
        # Tiêu đề
        self.title_label = ctk.CTkLabel(self, text="Hệ Thống Tìm kiếm",
                                        font=ctk.CTkFont(size=16, weight="bold"))
        self.title_label.pack(pady=10)

        # Khung tìm kiếm
        self.search_options_frame = ctk.CTkFrame(self)
        self.search_options_frame.pack(fill="x", padx=10, pady=5)

        self.search_label = ctk.CTkLabel(self.search_options_frame, text="Tìm kiếm theo:")
        self.search_label.pack(side="left", padx=10)

        self.search_type_var = ctk.StringVar(value="ID Nhân viên")
        self.search_type_options = ["ID Nhân viên", "Họ Tên", "Phòng ban", "Chức vụ"]
        self.search_type_menu = ctk.CTkOptionMenu(self.search_options_frame, variable=self.search_type_var,
                                                  values=self.search_type_options)
        self.search_type_menu.pack(side="left", padx=10)

        # Ô tìm kiếm
        self.search_box_frame = ctk.CTkFrame(self)
        self.search_box_frame.pack(fill="x", padx=10, pady=5)

        self.search_entry = ctk.CTkEntry(self.search_box_frame, placeholder_text="Nhập từ khóa tìm kiếm...", width=400)
        self.search_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        self.search_button = ctk.CTkButton(self.search_box_frame, text="Tìm kiếm", fg_color="#e74c3c",
                                           hover_color="#c0392b",
                                           command=self.search_employees)
        self.search_button.pack(side="left", padx=10, pady=10)

        self.view_all_button = ctk.CTkButton(self.search_box_frame, text="Làm mới", fg_color="#e74c3c",
                                             hover_color="#c0392b", command=self.load_employee_data)
        self.view_all_button.pack(side="left", padx=10, pady=10)

        # Bảng dữ liệu
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header
        self.header_frame = ctk.CTkFrame(self.table_frame)
        self.header_frame.pack(fill="x", padx=5, pady=5)

        # Các tiêu đề cột
        columns = ["ID", "Họ Tên", "Phòng ban", "Giới tính", "Chức vụ", "CMND/CCCD"]
        column_widths = [50, 150, 100, 100, 120, 100]

        for i, col in enumerate(columns):
            header_label = ctk.CTkLabel(self.header_frame, text=col, width=column_widths[i],
                                        font=ctk.CTkFont(weight="bold"))
            header_label.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")

        self.header_frame.grid_columnconfigure(len(columns), weight=1)

        # Khung cuộn cho dữ liệu
        self.table_data_frame = ctk.CTkScrollableFrame(self.table_frame)
        self.table_data_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def load_employee_data(self):
        for widget in self.table_data_frame.winfo_children():
            widget.destroy()
        self.selected_row = None
        self.row_frames = []
        employees = self.db_manager.get_all_employees()
        self.display_employees(employees)

    def search_employees(self):
        search_term = self.search_entry.get()
        search_type = self.search_type_var.get()
        for widget in self.table_data_frame.winfo_children():
            widget.destroy()
        self.selected_row = None
        self.row_frames = []
        employees = self.db_manager.search_employees(search_type, search_term)
        self.display_employees(employees)

    def display_employees(self, employees):
        column_widths = [50, 150, 100, 100, 120, 100]
        for i, employee in enumerate(employees):
            row_frame = ctk.CTkFrame(self.table_data_frame)
            row_frame.pack(fill="x", padx=5, pady=2)
            # Lưu lại ID để sử dụng trong các sự kiện
            row_frame.employee_id = employee["id_employee"]
            # Thêm vào danh sách để quản lý
            self.row_frames.append(row_frame)

            # ID
            id_label = ctk.CTkLabel(row_frame, text=employee["id_employee"], width=column_widths[0])
            id_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

            # Họ tên
            name_label = ctk.CTkLabel(row_frame, text=employee["name"], width=column_widths[1])
            name_label.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

            # Bộ phận
            dept_label = ctk.CTkLabel(row_frame, text=employee["department"], width=column_widths[2])
            dept_label.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

            # Giới tính
            branch_label = ctk.CTkLabel(row_frame, text=employee["gender"], width=column_widths[3])
            branch_label.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

            # Chức vụ
            position_label = ctk.CTkLabel(row_frame, text=employee["position"], width=column_widths[4])
            position_label.grid(row=0, column=4, padx=5, pady=5, sticky="nsew")

            # CMND/CCCD
            id_card_label = ctk.CTkLabel(row_frame, text=employee["cccd"], width=column_widths[5])
            id_card_label.grid(row=0, column=5, padx=5, pady=5, sticky="nsew")

            # Thêm bắt sự kiện click cho khung hàng
            row_frame.bind("<ButtonRelease-1>", lambda e, rf=row_frame: self.select_row(rf))

            # Thêm bắt sự kiện click cho từng widget trong hàng
            for widget in row_frame.winfo_children():
                widget.bind("<ButtonRelease-1>", lambda e, rf=row_frame: self.select_row(rf))

    def select_row(self, row_frame):
        # Nếu đã có hàng được chọn trước đó, đổi màu về mặc định
        if self.selected_row:
            self.selected_row.configure(fg_color=self.default_row_color)

        # Đổi màu hàng được chọn
        row_frame.configure(fg_color=self.selected_row_color)

        # Cập nhật hàng được chọn
        self.selected_row = row_frame

        # Gọi callback để xử lý khi chọn nhân viên
        if self.edit_callback:
            self.edit_callback(row_frame.employee_id)

    def set_edit_callback(self, callback):
        self.edit_callback = callback