# frontend/screens/screen_home.py

import customtkinter as ctk
from PIL import Image, ImageTk
import os
import tkinter as tk

class HomeScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color="transparent")

        # Load logo image
        self.logo_img = ctk.CTkImage(
            light_image=Image.open(os.path.join( "assets", "logo.png")),
            dark_image=Image.open(os.path.join( "assets", "logo.png")),
            size=(150, 150)
        )

        # Main container with scrollable frame
        self.main_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        # Logo
        logo_label = ctk.CTkLabel(header_frame, image=self.logo_img, text="")
        logo_label.pack(pady=(0, 20))

        title = ctk.CTkLabel(
            header_frame, 
            text="HỆ THỐNG CHẤM CÔNG THÔNG MINH", 
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="black",
            wraplength=700  # Wrap text if window is too small
        )
        title.pack()

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Sử dụng công nghệ nhận diện khuôn mặt",
            font=ctk.CTkFont(size=16),
            text_color="black",  # Light gray
            wraplength=600
        )
        subtitle.pack(pady=(5, 0))

        # Content area with two columns
        content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, pady=20)

        # Left column - Illustration
        illustration_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        illustration_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Create a regular tkinter label for the GIF
        self.gif_label = tk.Label(illustration_frame)
        self.gif_label.pack(expand=True)
        
        # Load and animate the GIF
        self.gif_frames = []
        self.current_frame = 0
        self.load_gif(os.path.join( "assets", "illustration.gif"))
        self.animate_gif()

        # Right column - Buttons
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Welcome message
        welcome_text = ctk.CTkLabel(
            button_frame,
            text="Chào mừng bạn!",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="black"
        )
        welcome_text.pack(pady=(0, 10))

        desc_text = ctk.CTkLabel(
            button_frame,
            text="Vui lòng chọn một trong các tùy chọn sau:",
            font=ctk.CTkFont(size=14),
            text_color="black",  # Light gray
            wraplength=300
        )
        desc_text.pack(pady=(0, 20))

        # Button container to ensure minimum width
        button_container = ctk.CTkFrame(button_frame, fg_color="transparent")
        button_container.pack(fill="x", padx=20)
        
        # Enhanced buttons with glowing effect
        login_btn = ctk.CTkButton(
            button_container, 
            text="Đăng nhập quản trị",
            command=controller.show_login,
            width=250,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#0078D4", "#005FB8"),  # Microsoft Blue
            hover_color=("#006ABC", "#004C99"),
            corner_radius=10
        )
        login_btn.pack(pady=10, fill="x")

        attendance_btn = ctk.CTkButton(
            button_container,
            text="Điểm danh bằng khuôn mặt",
            command=controller.show_attendance,
            width=250,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#0078D4", "#005FB8"),  # Microsoft Blue
            hover_color=("#006ABC", "#004C99"),
            corner_radius=10
        )
        attendance_btn.pack(pady=10, fill="x")

        # Footer
        footer_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        footer_frame.pack(fill="x", pady=(20, 0))

        footer_text = ctk.CTkLabel(
            footer_frame,
            text="© 2024 Face Recognition Attendance System | Developed by Nhóm tôi",
            font=ctk.CTkFont(size=12),
            text_color="#e0e0e0",  # Light gray
            wraplength=600
        )
        footer_text.pack()

        # Version info
        version_text = ctk.CTkLabel(
            footer_frame,
            text="Version 1.0.0",
            font=ctk.CTkFont(size=12),
            text_color="#e0e0e0"  # Light gray
        )
        version_text.pack()

    def load_gif(self, gif_path):
        """Load GIF frames"""
        gif = Image.open(gif_path)
        try:
            while True:
                frame = gif.copy()
                frame = frame.resize((400, 300), Image.Resampling.LANCZOS)
                self.gif_frames.append(ImageTk.PhotoImage(frame))
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

    def animate_gif(self):
        """Animate the GIF"""
        if self.gif_frames:
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            self.gif_label.configure(image=self.gif_frames[self.current_frame])
            self.after(100, self.animate_gif)  # Update every 100ms
