import pygame
import os
import time


Base_path = "E:/PythonProjectMain/"
Voice_path = os.path.join(Base_path,"AI/Voice/")

class Speech:
    def __init__(self):
        pygame.mixer.init()
        self.nhin_thang = pygame.mixer.Sound(os.path.join(Voice_path, "Vui_long_nhin_thang.mp3"))
        self.xoay_phai = pygame.mixer.Sound(os.path.join(Voice_path, "Vui_long_xoay_phai.mp3"))
        self.xoay_trai = pygame.mixer.Sound(os.path.join(Voice_path, "Vui_long_xoay_trai.mp3"))

    def Nhin_thang_start(self):
        self.nhin_thang.play()
        time.sleep(self.nhin_thang.get_length() - 0.6)

    def Xoay_phai_start(self):
        self.xoay_phai.play()
        time.sleep(self.xoay_phai.get_length() - 0.6)

    def Xoay_trai_start(self):
        self.xoay_trai.play()
        time.sleep(self.xoay_trai.get_length() - 0.6)

def main():
    speech = Speech()
    speech.Nhin_thang_start()
    speech.Xoay_phai_start()
    speech.Xoay_trai_start()

if __name__ == "__main__":
    main()
