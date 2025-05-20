import pygame
import os
import time

Base_path = "E:/PythonProjectMain/"
Voice_path = os.path.join(Base_path,"AI/Voice/")

class Speech:
    def __init__(self):
        pygame.mixer.init()
        self.nhin_thang = pygame.mixer.Sound(os.path.join(Voice_path, "Vui_long_nhin_thang.wav"))
        self.xoay_phai = pygame.mixer.Sound(os.path.join(Voice_path, "Vui_long_xoay_phai.wav"))
        self.xoay_trai = pygame.mixer.Sound(os.path.join(Voice_path, "Vui_long_xoay_trai.wav"))
        self.khong_ngua = pygame.mixer.Sound(os.path.join(Voice_path, "Vui_long_khong_ngua_mat.wav"))
        self.khong_cui = pygame.mixer.Sound(os.path.join(Voice_path, "Vui_long_khong_cui_mat.wav"))

    def Nhin_thang_start(self):
        self.nhin_thang.play()
        time.sleep(0.001)

    def Xoay_phai_start(self):
        self.xoay_phai.play()
        time.sleep(0.0001)

    def Xoay_trai_start(self):
        self.xoay_trai.play()
        time.sleep(0.0001)

    def Khong_ngua_start(self):
        self.khong_ngua.play()
        time.sleep(0.0001)

    def Khong_cui_start(self):
        self.khong_cui.play()
        time.sleep(0.0001)


def main():
    speech = Speech()
    last_play_time = time.time()
    for i in range(10000000):
        print(i)
        current_time = time.time()
        if current_time - last_play_time >= 5:
            speech.Nhin_thang_start()
            last_play_time = current_time
        #speech.Nhin_thang_start()
"""    speech.Nhin_thang_start()
    speech.Xoay_phai_start()
    speech.Xoay_trai_start()
    speech.Khong_ngua_start()
    speech.Khong_cui_start()
"""
if __name__ == "__main__":
    main()
