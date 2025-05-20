import pygame
import time

# Khởi tạo pygame mixer
pygame.mixer.init()

# Tải file mp3
sound = pygame.mixer.Sound("E:/PythonProjectMain/AI/Voice/Vui_long_nhin_thang.mp3")

# Phát nhạc
sound.play()

# Đợi đến khi nhạc kết thúc

time.sleep(sound.get_length())
print("Nhạc kết thúc")
