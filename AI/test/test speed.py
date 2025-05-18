import pygame
import time

# Khởi tạo pygame mixer
pygame.mixer.init()

# Tải file mp3
pygame.mixer.music.load("/AI/Voice/Vui_long_nhin_thang.mp3")

# Phát nhạc
pygame.mixer.music.play()

# Đợi đến khi nhạc kết thúc
while pygame.mixer.music.get_busy():
    time.sleep(1)
