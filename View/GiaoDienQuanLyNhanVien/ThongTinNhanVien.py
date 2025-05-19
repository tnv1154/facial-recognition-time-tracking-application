import customtkinter as ctk
from datetime import datetime
from View.ManagerView.GiaoDienTaiKhoan import Tao_giao_dien_tai_khoan
from AI.src.face_add_cam import FaceAdd, face_re_train
from Service.Salary_Service import SalaryService

class EmployeeInfoFrame(ctk.CTkFrame):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db_manager = db_manager
        self.current_employee_id = None
        self.setup_ui()

    def setup_ui(self):
        # Tiêu đề
        self.title_label = ctk.CTkLabel(self, text="Thông tin Nhân viên",
                                        font=ctk.CTkFont(size=16, weight="bold"))
        self.title_label.pack(pady=10)

        # Thông tin bộ phận
        self.dept_frame = ctk.CTkFrame(self)
        self.dept_frame.pack(fill="x", padx=10, pady=5)

        self.dept_title = ctk.CTkLabel(self.dept_frame, text="Thông tin phòng ban",
                                       font=ctk.CTkFont(weight="bold"))
        self.dept_title.pack(anchor="w", padx=10, pady=5)

        # Bộ phận
        self.dept_info_frame = ctk.CTkFrame(self.dept_frame)
        self.dept_info_frame.pack(fill="x", padx=10, pady=5)

        # Bộ phận
        self.dept_label = ctk.CTkLabel(self.dept_info_frame, text="Phòng ban:")
        self.dept_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.dept_var = ctk.StringVar(value="Nhân sự")
        self.dept_options = ["Nhân sự", "Quản lý", "Tài chính", "Kinh doanh"]
        self.dept_dropdown = ctk.CTkOptionMenu(self.dept_info_frame, variable=self.dept_var, values=self.dept_options)
        self.dept_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.personal_frame = ctk.CTkFrame(self)
        self.personal_frame.pack(fill="x", padx=10, pady=5)
        self.personal_title = ctk.CTkLabel(self.personal_frame, text="Thông tin cá nhân",
                                           font=ctk.CTkFont(weight="bold"))
        self.personal_title.pack(anchor="w", padx=10, pady=5)

        # Form thông tin cá nhân
        self.form_frame = ctk.CTkFrame(self.personal_frame)
        self.form_frame.pack(fill="x", padx=10, pady=5)

        # ID Nhân viên
        self.id_label = ctk.CTkLabel(self.form_frame, text="ID Nhân viên:")
        self.id_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.id_entry = ctk.CTkEntry(self.form_frame, width=200)
        self.id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.id_entry.insert(0, self.db_manager.get_max_id_employee())
        # Tên Nhân viên
        self.name_label = ctk.CTkLabel(self.form_frame, text="Tên Nhân viên:")
        self.name_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        self.name_entry = ctk.CTkEntry(self.form_frame, width=200)
        self.name_entry.grid(row=0, column=3, padx=10, pady=5, sticky="w")

        # Chức vụ
        self.position_label = ctk.CTkLabel(self.form_frame, text="Chức vụ:")
        self.position_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.position_var = ctk.StringVar(value="Nhân viên")
        self.position_options = ["Nhân viên", "Trưởng nhóm", "Trưởng phòng", "Giám đốc"]
        self.position_dropdown = ctk.CTkOptionMenu(self.form_frame, variable=self.position_var,
                                                   values=self.position_options)
        self.position_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # CMND/CCCD
        self.id_card_label = ctk.CTkLabel(self.form_frame, text="CMND/CCCD:")
        self.id_card_label.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        self.id_card_entry = ctk.CTkEntry(self.form_frame, width=200)
        self.id_card_entry.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        # Giới tính
        self.gender_label = ctk.CTkLabel(self.form_frame, text="Giới tính:")
        self.gender_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.gender_var = ctk.StringVar(value="Nam")

        self.gender_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.gender_frame.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.male_radio = ctk.CTkRadioButton(self.gender_frame, text="Nam", variable=self.gender_var, value="Nam")
        self.male_radio.pack(side="left", padx=(0, 20))

        self.female_radio = ctk.CTkRadioButton(self.gender_frame, text="Nữ", variable=self.gender_var, value="Nữ")
        self.female_radio.pack(side="left")

        # Ngày sinh
        self.birth_label = ctk.CTkLabel(self.form_frame, text="Ngày sinh:")
        self.birth_label.grid(row=2, column=2, padx=10, pady=5, sticky="w")

        self.birth_entry = ctk.CTkEntry(self.form_frame, width=200, placeholder_text="DD-MM-YYYY")
        self.birth_entry.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        # Email
        self.email_label = ctk.CTkLabel(self.form_frame, text="Email:")
        self.email_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.email_entry = ctk.CTkEntry(self.form_frame, width=200)
        self.email_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # SĐT
        self.phone_label = ctk.CTkLabel(self.form_frame, text="SĐT:")
        self.phone_label.grid(row=3, column=2, padx=10, pady=5, sticky="w")

        self.phone_entry = ctk.CTkEntry(self.form_frame, width=200)
        self.phone_entry.grid(row=3, column=3, padx=10, pady=5, sticky="w")

        # Địa chỉ
        self.address_label = ctk.CTkLabel(self.form_frame, text="Địa chỉ:")
        self.address_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.address_entry = ctk.CTkEntry(self.form_frame, width=200)
        self.address_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Trạng thái
        self.status_label = ctk.CTkLabel(self.form_frame, text="Trạng thái:")
        self.status_label.grid(row=4, column=2, padx=10, pady=5, sticky="w")

        self.status_var = ctk.StringVar(value="Đang làm việc")

        self.status_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.status_frame.grid(row=4, column=3, padx=10, pady=5, sticky="w")

        self.active_radio = ctk.CTkRadioButton(self.status_frame, text="Đang làm", variable=self.status_var,
                                               value="Đang làm")
        self.active_radio.pack(side="left", padx=(0, 20))

        self.inactive_radio = ctk.CTkRadioButton(self.status_frame, text="Đã nghỉ", variable=self.status_var,
                                                 value="Đã nghỉ")
        self.inactive_radio.pack(side="left")

        # Các nút chức năng
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(fill="x", padx=10, pady=10)

        # Thêm nhân viên mới
        self.add_button = ctk.CTkButton(self.button_frame, text="Thêm nhân viên mới", fg_color="#e74c3c",
                                        hover_color="#c0392b",
                                        command=self.add_new_employee)
        self.add_button.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        self.update_button = ctk.CTkButton(self.button_frame, text="Cập nhật", fg_color="#e74c3c",
                                           hover_color="#c0392b",
                                           command=self.update_employee)
        self.update_button.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        self.delete_button = ctk.CTkButton(self.button_frame, text="Xóa", fg_color="#e74c3c", hover_color="#c0392b",
                                           command=self.delete_employee)
        self.delete_button.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        self.clear_button = ctk.CTkButton(self.button_frame, text="Làm mới", fg_color="#e74c3c", hover_color="#c0392b",
                                          command=self.clear_form)
        self.clear_button.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        self.button_frame2 = ctk.CTkFrame(self)
        self.button_frame2.pack(fill="x", padx=10, pady=10)
        self.view_image = ctk.CTkButton(self.button_frame2, text="Xem ảnh nhân viên", fg_color="#e74c3c",corner_radius=10,
                                        hover_color="#c0392b",font=("Arial", 20, "bold"),height=40,width=60,
                                        command=self.view_image)
        self.view_image.pack(padx=150, pady=10)

    def add_new_employee(self):
        employee_data = {
            "id_employee": self.id_entry.get(),
            "name": self.name_entry.get(),
            "department": self.dept_var.get(),
            "position": self.position_var.get(),
            "cccd": self.id_card_entry.get(),
            "gender": self.gender_var.get(),
            "date_of_birth": self.birth_entry.get(),
            "email": self.email_entry.get(),
            "phonenumber": self.phone_entry.get(),
            "address": self.address_entry.get(),
            "status": self.status_var.get()
        }

        # Kiểm tra dữ liệu
        if not employee_data["id_employee"] or not employee_data["name"]:
            self.show_message("Lỗi", "ID và Tên Nhân viên không được để trống!")
            return
        if not employee_data["cccd"] or not employee_data["phonenumber"] :
            self.show_message("Lỗi", "CMND/CCCD và SĐT không được để trống!")
            return
        if not employee_data["date_of_birth"] or not employee_data["gender"] :
            self.show_message("Lỗi", "Giới tính và Ngày sinh không được để trống!")
            return
        # Thêm nhân viên mới
        face_add = FaceAdd(employee_data['id_employee'])
        if self.db_manager.add_employee(employee_data):
            self.show_message("Thành công", f"Đã thêm nhân viên {employee_data['name']} vào hệ thống!")
            self.clear_form()
        else:
            self.show_message("Lỗi", f"ID nhân viên {employee_data['id_employee']} đã tồn tại!")

    def update_employee(self):
        if not self.current_employee_id:
            self.show_message("Lỗi", "Vui lòng chọn nhân viên cần cập nhật từ danh sách!")
            return
        employee_data = {
            "id_employee": self.id_entry.get(),
            "name": self.name_entry.get(),
            "department": self.dept_var.get(),
            "position": self.position_var.get(),
            "cccd": self.id_card_entry.get(),
            "gender": self.gender_var.get(),
            "date_of_birth": self.birth_entry.get(),
            "email": self.email_entry.get(),
            "phonenumber": self.phone_entry.get(),
            "address": self.address_entry.get(),
            "status": self.status_var.get()
        }
        if not employee_data["id_employee"] or not employee_data["name"] :
            self.show_message("Lỗi", "ID và Tên Nhân viên không được để trống!")
            return
        if not employee_data["cccd"] or not employee_data["phonenumber"] :
            self.show_message("Lỗi", "CMND/CCCD và SĐT không được để trống!")
            return
        if not employee_data["date_of_birth"] or not employee_data["gender"] :
            self.show_message("Lỗi", "Giới tính và Ngày sinh không được để trống!")
            return

        if self.db_manager.update_employee(self.current_employee_id, employee_data):
            self.show_message("Thành công", f"Đã cập nhật thông tin nhân viên {employee_data['name']}!")

            self.current_employee_id = employee_data["id_employee"]
        else:
            self.show_message("Lỗi", "Không thể cập nhật thông tin nhân viên!")

    def delete_employee(self):
        if not self.current_employee_id:
            self.show_message("Lỗi", "Vui lòng chọn nhân viên cần xóa từ danh sách!")
            return

        employee = self.db_manager.get_employee_by_id(self.current_employee_id)
        if employee:
            confirm = self.show_confirm_dialog("Xác nhận", f"Bạn có chắc chắn muốn xóa nhân viên {employee['name']}?")
            if confirm:
                salarySer = SalaryService()
                salarySer.delete_salary_by_employee(self.current_employee_id)
                if self.db_manager.delete_employee(self.current_employee_id):
                    self.show_message("Thành công", f"Đã xóa nhân viên {employee['name']}!")
                    face_re_train(self.current_employee_id) #Xóa bộ phân loại và huấn luyện lại
                    self.clear_form()
                else:
                    self.show_message("Lỗi", "Không thể xóa nhân viên!")
        else:
            self.show_message("Lỗi", "Không tìm thấy thông tin nhân viên!")

    def clear_form(self):
        self.current_employee_id = None
        self.id_entry.delete(0, 'end')
        self.id_entry.insert(0, self.db_manager.get_max_id_employee())
        self.name_entry.delete(0, 'end')
        self.id_card_entry.delete(0, 'end')
        self.birth_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.address_entry.delete(0, 'end')

        # Reset các giá trị mặc định
        self.dept_var.set("Nhân sự")
        self.position_var.set("Nhân viên")
        self.gender_var.set(None)
        self.status_var.set("Đang làm")

    def load_employee_data(self, employee_id):
        # Lấy thông tin nhân viên từ database
        employee = self.db_manager.get_employee_by_id(employee_id)
        if employee:
            self.current_employee_id = employee_id
            # Điền dữ liệu vào form
            self.id_entry.delete(0, 'end')
            self.id_entry.insert(0, employee["id_employee"])
            self.name_entry.delete(0, 'end')
            self.name_entry.insert(0, employee["name"])
            self.dept_var.set(employee["department"])
            self.position_var.set(employee["position"])
            self.id_card_entry.delete(0, 'end')
            self.id_card_entry.insert(0, employee["cccd"])
            self.gender_var.set(employee["gender"])
            self.birth_entry.delete(0, 'end')
            self.birth_entry.insert(0, employee["date_of_birth"])
            self.email_entry.delete(0, 'end')
            self.email_entry.insert(0, employee["email"])
            self.phone_entry.delete(0, 'end')
            self.phone_entry.insert(0, employee["phonenumber"])
            self.address_entry.delete(0, 'end')
            self.address_entry.insert(0, employee["address"])
            self.status_var.set(employee["status"])

    def show_message(self, title, message):

        messagebox = ctk.CTkToplevel(self)
        messagebox.title(title)
        messagebox.geometry("300x150")
        messagebox.resizable(False, False)

        messagebox.update_idletasks()
        width = messagebox.winfo_width()
        height = messagebox.winfo_height()
        x = (messagebox.winfo_screenwidth() // 2) - (width // 2)
        y = (messagebox.winfo_screenheight() // 2) - (height // 2)
        messagebox.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        messagebox.transient(self)
        messagebox.grab_set()
        # Nội dung thông báo
        msg_label = ctk.CTkLabel(messagebox, text=message, wraplength=250)
        msg_label.pack(pady=20)
        ok_button = ctk.CTkButton(messagebox, text="OK", command=messagebox.destroy)
        ok_button.pack(pady=10)

        messagebox.wait_window()

    def show_confirm_dialog(self, title, message):
        """Hiển thị hộp thoại xác nhận và trả về lựa chọn của người dùng"""
        result = [False]  # Sử dụng list để có thể thay đổi giá trị từ các hàm callback

        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("350x150")
        dialog.resizable(False, False)

        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        # Thiết lập là modal dialog
        dialog.transient(self)
        dialog.grab_set()

        # Nội dung thông báo
        msg_label = ctk.CTkLabel(dialog, text=message, wraplength=300)
        msg_label.pack(pady=20)

        # Frame chứa các nút
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=10)

        # Nút chấp nhận
        def on_confirm():
            result[0] = True
            dialog.destroy()

        confirm_button = ctk.CTkButton(button_frame, text="Xác nhận", fg_color="#e74c3c", hover_color="#c0392b",
                                       command=on_confirm)
        confirm_button.pack(side="left", padx=10)

        # Nút hủy
        cancel_button = ctk.CTkButton(button_frame, text="Hủy", command=dialog.destroy)
        cancel_button.pack(side="left", padx=10)

        dialog.wait_window()
        return result[0]
    def view_image(self):
        if not self.current_employee_id:
            self.show_message("Lỗi", "Vui lòng chọn nhân viên cần cập nhật từ danh sách!")
            return
        windows =ctk.CTkToplevel()
        windows.title("Thông tin nhân viên")
        windows.attributes("-topmost", True)
        Tao_giao_dien_tai_khoan().tao_giao_dien_tai_khoan(windows,self.id_entry.get())

