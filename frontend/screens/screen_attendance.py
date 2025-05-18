import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import cv2
from AI.src.face_rec_cam import FaceRecognitionCam
from Service.Employee_Service import EmployeeService
from View.GiaoDienThongKe.LayDuLieu import employees
from collections import Counter
from Service.Timekeeping_Service import TimekeepingService
import time
import numpy as np

# Cấu hình thư viện customtkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class AttendanceScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color="transparent")
        self.controller = controller  # Lưu controller để sử dụng sau này

        # Biến để lưu trạng thái camera
        self.camera = None
        self.is_camera_running = False
        
        # Khởi tạo đối tượng nhận diện khuôn mặt
        self.face_recognizer = None
        
        # Biến đếm thời gian để xác định khi nào lấy ID
        self.frame_count = 0
        self.detected_id = None
        self.recognition_done = False
        
        # Biến thời gian để reset trạng thái nhận diện
        self.last_recognition_time = 0
        self.recognition_cooldown = 3  # Thời gian chờ (giây) trước khi sẵn sàng nhận diện mặt mới

        # Nút quay lại
        back_button = ctk.CTkButton(
            self,
            text="Quay lại",
            command=self.controller.show_home,
            font=("Arial", 12, "bold"),
            fg_color="#000080",
            width=100,
            height=30
        )
        back_button.pack(anchor="nw", padx=10, pady=10)

        # Tiêu đề - Có thể thay đổi màu chữ ở đây
        title_label = ctk.CTkLabel(self, text="Hệ thống chấm công khuôn mặt",
                                   font=("Arial", 24, "bold"),
                                   text_color="#FF0000")  # Thay đổi màu chữ ở đây
        title_label.pack(pady=10)

        # Frame chính chứa các phần tử
        main_frame = ctk.CTkFrame(self, fg_color="white")
        main_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # ==== PHẦN BÊN TRÁI ====
        left_frame = ctk.CTkFrame(main_frame, fg_color="white", border_width=2, border_color="gray")
        left_frame.pack(side="left", fill="both", expand=True, padx=5)

        # Tạo frame mới ở dưới cùng để chứa thông báo và nút
        bottom_controls_frame = ctk.CTkFrame(left_frame, fg_color="white")
        bottom_controls_frame.pack(fill="x", pady=5, side="bottom")

        # Frame cho phần nhận diện
        recognition_frame = ctk.CTkFrame(left_frame, fg_color="white", border_width=1, border_color="gray")
        recognition_frame.pack(fill="x", pady=10, padx=10)

        # Có thể thay đổi màu chữ ở đây
        recognition_label = ctk.CTkLabel(recognition_frame, text="Màn hình nhận diện",
                                         font=("Arial", 12, "bold"),
                                         text_color="black")  # Thay đổi màu chữ ở đây
        recognition_label.pack(anchor="w", padx=10, pady=5)

        # Chọn loại chấm công
        frame_top = ctk.CTkFrame(recognition_frame, fg_color="white")
        frame_top.pack(pady=10, fill="x", padx=10)

        # Có thể thay đổi màu chữ ở đây
        type_label = ctk.CTkLabel(frame_top, text="Chọn loại Chấm công:",
                                  font=("Arial", 12),
                                  text_color="black")  # Thay đổi màu chữ ở đây
        type_label.pack(side="left", padx=5)

        self.type_combobox = ctk.CTkComboBox(frame_top, values=["Check in", "Check out"],
                                             width=300, height=30)
        self.type_combobox.pack(side="left", padx=5)

        # Khung danh sách nhận diện
        self.face_frame = ctk.CTkFrame(left_frame, fg_color="white", border_width=1,
                                       border_color="gray", width=640, height=640)  # Tăng chiều cao từ 480 lên 640
        self.face_frame.pack(padx=10, pady=10)
        self.face_frame.pack_propagate(False)  # Ngăn không cho frame tự động mở rộng

        # Thêm label để hiển thị camera
        self.camera_label = tk.Label(self.face_frame, bg="black")
        self.camera_label.pack(fill="both", expand=True)

        # Thông báo phía dưới - Có thể thay đổi màu chữ ở đây
        self.notice_label = ctk.CTkLabel(bottom_controls_frame,
                                         text="Thông báo: Vui lòng chọn loại chấm công để mở Camera",
                                         text_color="#FF0000",  # Thay đổi màu chữ ở đây
                                         font=("Arial", 11))
        self.notice_label.pack(pady=5)

        # Nút mở / đóng camera
        button_frame = ctk.CTkFrame(bottom_controls_frame, fg_color="white")
        button_frame.pack(pady=5)

        # Tạo frame con để căn giữa các nút
        button_container = ctk.CTkFrame(button_frame, fg_color="white")
        button_container.pack(expand=True)

        self.start_button = ctk.CTkButton(button_container, text="Mở Camera",
                                          font=("Arial", 12, "bold"),
                                          fg_color="#000080",
                                          width=200,
                                          height=35,
                                          command=self.start_camera)
        self.start_button.pack(side="left", padx=(50, 20))

        self.stop_button = ctk.CTkButton(button_container, text="Đóng Camera",
                                         font=("Arial", 12, "bold"),
                                         fg_color="#000080",
                                         width=200,
                                         height=35,
                                         command=self.stop_camera)
        self.stop_button.pack(side="left", padx=(20, 50))

        # Vô hiệu hóa nút đóng camera ban đầu
        self.stop_button.configure(state="disabled")

        # ==== PHẦN BÊN PHẢI ====
        right_frame = ctk.CTkFrame(main_frame, fg_color="white", border_width=2, border_color="gray")
        right_frame.pack(side="left", fill="both", expand=True, padx=5)

        # Frame trên - Điểm danh thành công và thông tin nhân viên
        top_right_frame = ctk.CTkFrame(right_frame, fg_color="white", border_width=1, border_color="gray")
        top_right_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Có thể thay đổi màu chữ ở đây
        success_label = ctk.CTkLabel(top_right_frame, text="Chấm công thành công",
                                     font=("Arial", 14, "bold"),
                                     text_color="black")  # Thay đổi màu chữ ở đây
        success_label.pack(pady=10)

        # Khung hình ảnh khuôn mặt
        image_frame = ctk.CTkFrame(top_right_frame, fg_color="white", border_width=1, border_color="gray")
        image_frame.pack(pady=10, padx=10)

        # Load ảnh mặc định (dấu hỏi)
        default_image = Image.open("E:\\PythonProject\\frontend\\assets\\default_avatar.png")
        default_image = default_image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(default_image)
        self.img_label = ctk.CTkLabel(image_frame, image=self.photo, text="")
        self.img_label.pack(pady=5)

        # Thông tin nhân viên
        self.employee_info = {
            "id": "",
            "name": "",
            "time": ""
        }

        info_content = ctk.CTkFrame(top_right_frame, fg_color="white", border_width=1, border_color="gray")
        info_content.pack(fill="x", padx=10, pady=10)

        # Có thể thay đổi màu chữ ở đây
        self.id_label = ctk.CTkLabel(info_content, text="ID Nhân viên:",
                                     font=("Arial", 12),
                                     text_color="black")  # Thay đổi màu chữ ở đây
        self.id_label.pack(anchor="w", padx=10, pady=5)

        # Có thể thay đổi màu chữ ở đây
        self.name_label = ctk.CTkLabel(info_content, text="Tên Nhân viên:",
                                       font=("Arial", 12),
                                       text_color="black")  # Thay đổi màu chữ ở đây
        self.name_label.pack(anchor="w", padx=10, pady=5)

        # Có thể thay đổi màu chữ ở đây
        self.time_label = ctk.CTkLabel(info_content, text="Thời gian:",
                                       font=("Arial", 12),
                                       text_color="black")  # Thay đổi màu chữ ở đây
        self.time_label.pack(anchor="w", padx=10, pady=5)

        # Frame dưới - Thông tin nhân viên
        bottom_right_frame = ctk.CTkFrame(right_frame, fg_color="white", border_width=1, border_color="gray")
        bottom_right_frame.pack(fill="both", padx=5, pady=5)

        # Có thể thay đổi màu chữ ở đây
        info_title = ctk.CTkLabel(bottom_right_frame, text="Thông tin nhân viên",
                                  font=("Arial", 12, "bold"),
                                  text_color="black")  # Thay đổi màu chữ ở đây
        info_title.pack(anchor="w", padx=10, pady=5)

        # Có thể thay đổi màu chữ ở đây
        self.dept_label = ctk.CTkLabel(bottom_right_frame, text="Phòng ban: ",
                                       text_color="#FF0000",  # Thay đổi màu chữ ở đây
                                       font=("Arial", 12))
        self.dept_label.pack(anchor="w", padx=10)

        # Có thể thay đổi màu chữ ở đây
        self.position_label = ctk.CTkLabel(bottom_right_frame, text="Chức vụ: ",
                                           text_color="#FF0000",  # Thay đổi màu chữ ở đây
                                           font=("Arial", 12))
        self.position_label.pack(anchor="w", padx=10)


        #self.checkin_time_label.pack(anchor="w", padx=10, pady=(0, 5))

    def show_success_popup(self, employee_id, employee_name):
        """Hiển thị popup thông báo chấm công thành công"""
        popup = ctk.CTkToplevel(self)
        popup.title("Thông báo")
        popup.geometry("400x200")
        popup.resizable(False, False)
        
        # Đặt popup ở trên cùng
        popup.attributes('-topmost', True)
        
        # Frame chính
        main_frame = ctk.CTkFrame(popup, fg_color="white")
        main_frame.pack(expand=True, fill=None)
        
        # Icon thành công
        success_label = ctk.CTkLabel(main_frame, text="✓", font=("Arial", 40, "bold"), text_color="green")
        success_label.pack(pady=(10, 5))
        # Thông báo chấm công thành công
        message_label = ctk.CTkLabel(main_frame, text="Chấm công thành công!", 
                                   font=("Arial", 18, "bold"), text_color="green")
        message_label.pack(pady=5)
        # Thông tin nhân viên
        id_label = ctk.CTkLabel(main_frame, text=f"ID: {employee_id}", font=("Arial", 14))
        id_label.pack()
        
        name_label = ctk.CTkLabel(main_frame, text=f"Tên: {employee_name}", font=("Arial", 14))
        name_label.pack()
        # Nút OK
        ok_button = ctk.CTkButton(main_frame, text="OK", width=100, 
                                 command=popup.destroy, fg_color="#000080")
        ok_button.pack(pady=10)
        
        # Đặt popup ở giữa màn hình
        popup.update_idletasks()  # Cập nhật để lấy kích thước thực của popup
        
        # Lấy chiều rộng và chiều cao của màn hình
        width_screen = popup.winfo_screenwidth()
        height_screen = popup.winfo_screenheight()
        
        # Lấy chiều rộng và chiều cao của popup
        width_popup = popup.winfo_width()
        height_popup = popup.winfo_height()
        
        # Tính toán vị trí để đặt popup ở giữa màn hình
        x_position = (width_screen - width_popup) // 2
        y_position = (height_screen - height_popup) // 2
        
        # Đặt vị trí popup
        popup.geometry(f"+{x_position}+{y_position}")
        
        # Tự động đóng popup sau 3 giây
        popup.after(3000, popup.destroy)

    def format_time_range(self, check_time):
        """Tính toán và định dạng khoảng thời gian làm việc 8 tiếng"""
        # Chuyển đổi chuỗi thời gian thành đối tượng datetime
        start_time = datetime.strptime(check_time, "%H:%M")
        # Cộng thêm 8 tiếng
        end_time = start_time + timedelta(hours=8)
        # Định dạng lại thành chuỗi
        return f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"

    def update_employee_details(self, department, position, checkin_time):
        """Cập nhật thông tin chi tiết của nhân viên"""
        self.dept_label.configure(text=f"Phòng ban: {department}")
        self.position_label.configure(text=f"Chức vụ: {position}")
        # Hiển thị khoảng thời gian làm việc
        time_range = self.format_time_range(checkin_time)
        self.checkin_time_label.configure(text=f"Thời gian làm việc: {time_range}")

    def show_employee_info(self, employee_id, employee_name, check_time, department="", position=""):
        """Hiển thị thông tin nhân viên khi chấm công thành công"""
        # Cập nhật thông tin cơ bản
        self.employee_info["id"] = employee_id
        self.employee_info["name"] = employee_name
        self.employee_info["time"] = check_time

        # Cập nhật nội dung phần trên
        self.id_label.configure(text=f"ID Nhân viên: {employee_id}")
        self.name_label.configure(text=f"Tên Nhân viên: {employee_name}")
        self.time_label.configure(text=f"Thời gian: {check_time}")

        self.dept_label.configure(text=f"Phòng ban: {department}")
        self.position_label.configure(text=f"Chức vụ: {position}")

    def start_camera(self):
        """Mở camera và bắt đầu hiển thị hình ảnh"""
        if not self.is_camera_running:
            # Chuyển từ VideoStream sang cv2.VideoCapture
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                print("Không thể mở camera")
                self.notice_label.configure(text="Không thể mở camera", text_color="red")
                return
                
            self.is_camera_running = True
            
            # Khởi tạo đối tượng nhận diện khuôn mặt nếu chưa có
            if not self.face_recognizer:
                self.face_recognizer = FaceRecognitionCam()
            
            # Reset biến đếm frame và trạng thái nhận diện
            self.reset_recognition_state()
            
            # Cập nhật trạng thái nút
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")

            # Cập nhật thông báo
            self.notice_label.configure(text="Camera đang hoạt động - Đang nhận diện khuôn mặt...", text_color="green")

            # Bắt đầu hiển thị hình ảnh từ camera
            self.show_camera_feed()
        else:
            print("Camera đã đang chạy!")

    def reset_recognition_state(self):
        """Reset lại trạng thái nhận diện"""
        self.frame_count = 0
        self.detected_id = None
        self.recognition_done = False
        self.last_recognition_time = 0
        
        # Reset trạng thái của face_recognizer nếu cần
        if self.face_recognizer:
            self.face_recognizer.reset()
        
        # Cập nhật thông báo
        self.notice_label.configure(text="Đang nhận diện khuôn mặt...", text_color="green")

    def stop_camera(self):
        """Đóng camera và dừng hiển thị hình ảnh"""
        if self.is_camera_running and self.camera is not None:
            self.camera.release()
            self.is_camera_running = False

            # Cập nhật trạng thái nút
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")

            # Cập nhật thông báo
            self.notice_label.configure(text="Camera đã tắt", text_color="red")

            # Xóa hình ảnh hiện tại
            self.camera_label.configure(image="")

    def show_camera_feed(self):
        """Hiển thị hình ảnh từ camera và thực hiện nhận diện khuôn mặt"""
        if not self.is_camera_running or self.camera is None:
            return
            
        # Sử dụng camera.read() của OpenCV để đọc frame
        ret, frame = self.camera.read()
        if not ret:
            print("Không thể đọc frame từ camera")
            self.notice_label.configure(text="Không thể đọc frame từ camera", text_color="red")
            self.stop_camera()
            return
            
        # Chuyển đổi frame từ BGR sang RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Kiểm tra xem đã đủ thời gian để reset trạng thái nhận diện chưa
        current_time = time.time()
        if self.recognition_done and (current_time - self.last_recognition_time) > self.recognition_cooldown:
            self.reset_recognition_state()
        
        # Xử lý nhận diện khuôn mặt nếu chưa nhận diện xong
        if not self.recognition_done and self.face_recognizer:
            processed_frame, current_id = self.face_recognizer.process_frame(frame_rgb)
            
            # Tăng số frame đã xử lý
            self.frame_count += 1
            
            # Nếu phát hiện có ID, lưu lại
            if current_id is not None:
                self.detected_id = current_id
            
            # Sau khoảng 50 frame (~1.7 giây), kiểm tra ID và lấy thông tin nhân viên
            if self.frame_count >= 50 and self.detected_id is not None:
                self.recognition_done = True
                self.last_recognition_time = current_time
                
                # Xử lý trường hợp khuôn mặt không được nhận diện (UNKNOWN)
                if self.detected_id == "UNKNOWN":
                    current_time_str = datetime.now().strftime("%H:%M")
                    # Hiển thị thông tin UNKNOWN
                    self.show_employee_info(
                        "UNKNOWN", 
                        "UNKNOWN", 
                        current_time_str, 
                        "UNKNOWN", 
                        "UNKNOWN"
                    )
                    
                    # Đặt lại ảnh mặc định
                    default_image = Image.open("E:\\PythonProject\\frontend\\assets\\default_avatar.png")
                    default_image = default_image.resize((150, 150))
                    self.photo = ImageTk.PhotoImage(default_image)
                    self.img_label.configure(image=self.photo)
                    
                    # Cập nhật thông báo
                    self.notice_label.configure(
                        text=f"Không nhận diện được khuôn mặt - Sẵn sàng nhận diện tiếp trong {self.recognition_cooldown}s", 
                        text_color="orange"
                    )
                else:
                    # Lấy thông tin nhân viên từ ID nếu không phải UNKNOWN
                    try:
                        employee_service = EmployeeService()
                        employee = employee_service.get_employees_by_id_employee(self.detected_id)
                        current_time_str = datetime.now().strftime("%H:%M")

                        check = self.type_combobox.get()
                        print(check)
                        if check == "Check in":
                            TimekeepingService().check_in_employee(self.detected_id, current_time_str)
                        else:
                            TimekeepingService().check_out_employee(self.detected_id, current_time_str)
                        
                        # Hiển thị thông tin nhân viên
                        self.show_employee_info(
                            self.detected_id, 
                            employee["name"], 
                            current_time_str, 
                            employee["department"], 
                            employee["position"]
                        )
                        
                        # Hiển thị popup thông báo chấm công thành công
                        self.show_success_popup(self.detected_id, employee["name"])
                        
                        # Cập nhật thông báo
                        self.notice_label.configure(
                            text=f"Nhận diện thành công: {employee['name']} - ID: {self.detected_id} - Sẵn sàng nhận diện tiếp trong {self.recognition_cooldown}s", 
                            text_color="green"
                        )
                    except Exception as e:
                        print(f"Lỗi khi lấy thông tin nhân viên: {e}")
                        self.notice_label.configure(
                            text=f"Đã nhận diện ID: {self.detected_id}, nhưng không tìm thấy thông tin nhân viên - Sẵn sàng nhận diện tiếp trong {self.recognition_cooldown}s", 
                            text_color="orange"
                        )
        else:
            # Nếu đã nhận diện xong, tiếp tục hiển thị kết quả nhận diện
            if self.face_recognizer:
                processed_frame, _ = self.face_recognizer.process_frame(frame_rgb)
            else:
                processed_frame = frame_rgb
                
            # Cập nhật thông báo đếm ngược
            if self.recognition_done:
                remaining_time = max(0, self.recognition_cooldown - (current_time - self.last_recognition_time))
                if remaining_time > 0:
                    self.notice_label.configure(
                        text=f"Đã nhận diện: {self.employee_info['name']} - Sẵn sàng nhận diện tiếp trong {remaining_time:.1f}s", 
                        text_color="green"
                    )

        # Thay đổi kích thước frame để lấp đầy khung tối đa, chấp nhận cắt một phần để đảm bảo hiển thị lớn nhất
        h, w = processed_frame.shape[:2]
        target_width, target_height = 640, 640  # Kích thước khung đen
        
        # Tính toán tỷ lệ scale theo cả chiều rộng và chiều cao
        scale_w = target_width / w
        scale_h = target_height / h
        
        # Sử dụng tỷ lệ lớn hơn để đảm bảo lấp đầy khung (fill/cover)
        scale = max(scale_w, scale_h)
        
        # Tính kích thước mới sau khi scale
        new_width = int(w * scale)
        new_height = int(h * scale)
        
        # Thay đổi kích thước frame theo tỷ lệ mới
        frame_resized = cv2.resize(processed_frame, (new_width, new_height))
        
        # Tạo một khung hình đen có kích thước cố định
        display_frame = np.zeros((target_height, target_width, 3), dtype=np.uint8)
        
        # Tính toán vị trí để căn giữa hình ảnh trong khung
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2
        
        # Đặt hình ảnh đã resize vào khung đen, cắt bớt nếu vượt quá kích thước
        # Xác định phần của hình ảnh sẽ được hiển thị
        src_x = max(0, -x_offset)
        src_y = max(0, -y_offset)
        dst_x = max(0, x_offset)
        dst_y = max(0, y_offset)
        
        # Tính chiều rộng và chiều cao của phần hiển thị
        width_to_copy = min(new_width - src_x, target_width - dst_x)
        height_to_copy = min(new_height - src_y, target_height - dst_y)
        
        if width_to_copy > 0 and height_to_copy > 0:
            # Sao chép phần của hình ảnh vào khung hiển thị
            display_frame[dst_y:dst_y+height_to_copy, dst_x:dst_x+width_to_copy] = \
                frame_resized[src_y:src_y+height_to_copy, src_x:src_x+width_to_copy]

        # Chuyển đổi frame thành ảnh PIL
        image = Image.fromarray(display_frame)
        photo = ImageTk.PhotoImage(image=image)

        # Hiển thị ảnh
        self.camera_label.configure(image=photo)
        self.camera_label.image = photo  # Giữ reference để tránh bị garbage collected

        # Cập nhật hình ảnh
        if self.is_camera_running:
            self.after(10, self.show_camera_feed)  # Cập nhật mỗi 10ms
        
    def __del__(self):
        """Đảm bảo camera được đóng khi đối tượng bị hủy"""
        if hasattr(self, 'camera') and self.camera is not None:
            self.camera.release()

