import customtkinter as ctk
from tkinter import messagebox
from Service.Account_Service import AccountService
from View.ManagerView.ManagerView import Tao_Giao_Dien_Chinh

class LoginApp:
    def __init__(self,root,container):
        self.root=root
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.Account = AccountService()
        self.accounts = self.Account.get_all_accounts()
        self.setup_login_ui(container)

    def setup_login_ui(self,container):
        # Nút quay lại
        top_bar = ctk.CTkFrame(container,fg_color="white")
        top_bar.pack(side=ctk.TOP, fill=ctk.X)
        return_frame = ctk.CTkButton(top_bar, text="◀ Quay lại",font=("Arial", 16, "bold"),command=self.root.show_home,
                                     corner_radius=20, fg_color="#0078D7", hover_color="#005A9E")
        return_frame.pack(side=ctk.LEFT, padx=10, pady=10, )

        # Frame chính
        main_frame = ctk.CTkFrame(container)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Tiêu đề
        title_label = ctk.CTkLabel(
            main_frame,
            text="HỆ THỐNG QUẢN LÝ NHÂN VIÊN",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#333333"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Tên đăng nhập
        username_label = ctk.CTkLabel(
            main_frame,
            text="Tên đăng nhập:",
            font=ctk.CTkFont(size=14)
        )
        username_label.grid(row=1, column=0, sticky="w", pady=5, padx=10)
        self.username_entry = ctk.CTkEntry(main_frame, width=200)
        self.username_entry.grid(row=1, column=1, pady=5, padx=10)

        # Mật khẩu
        password_label = ctk.CTkLabel(
            main_frame,
            text="Mật khẩu:",
            font=ctk.CTkFont(size=14)
        )
        password_label.grid(row=2, column=0, sticky="w", pady=5, padx=10)
        self.password_entry = ctk.CTkEntry(main_frame, width=200, show="*")
        self.password_entry.grid(row=2, column=1, pady=5, padx=10)

        # Nút đăng nhập
        login_button = ctk.CTkButton(
            main_frame,
            text="Đăng Nhập",font=("Arial", 16, "bold"),
            command=self.login,
            fg_color="#0078D7",
            hover_color="#005A9E",
            width=150
        )
        login_button.grid(row=3, column=0, columnspan=2, pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        if username in [a["username"] for a in self.accounts]:
            account_check = self.Account.get_account_by_username(username)
            if password == account_check["password"]:
                messagebox.showinfo("Thành công", "Đăng nhập thành công!")
                self.open_manager_view(account_check["id_employee"])
            else:
                messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")

    def open_manager_view(self, id_employee):
        self.root.withdraw()
        manager_view = ctk.CTkToplevel()
        employee_app = Tao_Giao_Dien_Chinh(self.root,manager_view, id_employee)
