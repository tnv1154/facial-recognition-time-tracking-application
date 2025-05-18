import customtkinter as ctk
from datetime import datetime
import locale
import pandas as pd
from tkinter import messagebox, filedialog
from View.GiaoDienThongKe.ThongKeChamCong import AttendancePage
from View.GiaoDienThongKe.BaoCaoChamCong import TimesheetPage
from View.GiaoDienThongKe.BaoCaoLuong import SalaryPage
from View.GiaoDienThongKe.LayDuLieu import employees, timekeepings, salarys

class Giao_Dien_Thong_Ke(ctk.CTk):
    def __init__(self,parents):
        self.parents=parents
        # Cấu hình cửa sổ chính
        self.parents.title("Thống kê")
        self.parents.geometry("1200x700")

        # Thiết lập theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

             # Tạo khung chứa tab
        self.tab_view = ctk.CTkTabview(self.parents, fg_color='#4a8fe7')
        self.tab_view.pack(expand=True, fill="both", padx=50, pady=50)
        # Tạo nút xuất Excel
        self.export_button = ctk.CTkButton(
            self.parents,
            text="Xuất Excel",
            command=self.export_to_excel,
            width=120,
            height=40,
            font=("Arial", 16),
            fg_color="#5CA9EB",  # Màu xanh của Excel
            hover_color="#4682B4"
        )
        self.export_button.place(relx=0.95, rely=0.02, anchor="ne")
        # Tạo các tab
        self.tab_view.add("Thống kê điểm danh")
        self.tab_view.add("Báo cáo chấm công")
        self.tab_view.add("Báo cáo lương")
        self.tab_view._segmented_button.configure(font=("Arial", 25),text_color="black")
        # Khởi tạo các trang
        self.attendance_page = AttendancePage(
            self.tab_view.tab("Thống kê điểm danh"),
            employees=employees,
            timekeepings=timekeepings
        )
        self.timesheet_page = TimesheetPage(
            self.tab_view.tab("Báo cáo chấm công"),
            employees=employees,
            timekeepings=timekeepings
        )
        self.salary_page = SalaryPage(
            self.tab_view.tab("Báo cáo lương"),
            employees=employees,
            salarys=salarys
        )

    def export_to_excel(self):
        try:
            current_tab = self.tab_view.get()
            if current_tab == "Thống kê điểm danh":
                headers, data = self.attendance_page.get_table_data()
                default_filename = "thong_ke_diem_danh.xlsx"
            elif current_tab == "Báo cáo chấm công":
                headers, data = self.timesheet_page.get_table_data()
                default_filename = "bao_cao_cham_cong.xlsx"
            elif current_tab == "Báo cáo lương":
                headers, data = self.salary_page.get_table_data()
                default_filename = "bao_cao_luong.xlsx"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                initialfile=default_filename,
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Lưu file Excel"
            )
            if not file_path:
                return
            # Tạo DataFrame và xuất ra Excel
            df = pd.DataFrame(data, columns=headers)
            # Tạo writer để định dạng Excel
            writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            # Lấy workbook và worksheet
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            # Định dạng header
            header_format = workbook.add_format({
                'bold': True,
                'font_size': 12,
                'bg_color': '#4a8fe7',
                'font_color': 'white',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'
            })
            # Định dạng cho các ô dữ liệu
            cell_format = workbook.add_format({
                'font_size': 11,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'
            })
            # Áp dụng định dạng cho header
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                worksheet.set_column(col_num, col_num, 15)  # Đặt độ rộng cột
            # Áp dụng định dạng cho dữ liệu
            for row_num in range(len(df)):
                for col_num in range(len(df.columns)):
                    worksheet.write(row_num + 1, col_num, df.iloc[row_num, col_num], cell_format)
            # Tự động điều chỉnh độ rộng cột
            for i, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(col)
                )
                worksheet.set_column(i, i, max_length + 2)
            # Lưu file
            writer.close()
            messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra file {file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file Excel: {str(e)}")
if __name__ == "__main__":
    app = ctk.CTk()
    giao_dien = Giao_Dien_Thong_Ke(app)
    app.mainloop()