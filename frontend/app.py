import customtkinter as ctk
from screens.screen_home import HomeScreen
import tensorflow as tf

# Khởi tạo giao diện chính
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Chấm công bằng khuôn mặt")
        self.geometry("800x600")
        self.minsize(800, 600)  # Set minimum window size
        
        # Set dark mode
        #self._set_appearance_mode("dark")
        # Set dark background color
        self.configure(fg_color="white") 

        # Khởi tạo container để hiển thị các screen
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.show_home()

    def show_home(self):
        # Xóa các widget hiện tại
        for widget in self.container.winfo_children():
            widget.destroy()
        HomeScreen(self.container, self).pack(fill="both", expand=True)

    def show_attendance(self):
        from screens.screen_attendance import AttendanceScreen
        for widget in self.container.winfo_children():
            widget.destroy()
        AttendanceScreen(self.container, self).pack(fill="both", expand=True)

    def show_login(self):
        from screens.screen_login import LoginApp
        for widget in self.container.winfo_children():
            widget.destroy()
        self.login=LoginApp(self,self.container)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = MainApp()
    app.mainloop()
