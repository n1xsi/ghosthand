import threading
import ctypes
import time


class AutoPistolCore:
    def __init__(self):
        self.running = False  # Глобальный переключатель потока
        self.enabled = False  # Переключатель функционала (чекбокс в меню)

    def _click(self):
        ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
    
    def _is_lbutton_down(self):
        # 0x05 - ближняя боковая кнопка, mouse4
        return ctypes.windll.user32.GetAsyncKeyState(0x05) & 0x8000

    def _loop(self):
        while self.running:
            if self.enabled:
                if self._is_lbutton_down():
                    self._click()
                    time.sleep(0.01)
            time.sleep(0.01)


    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

# Экземпляр класса AutoPistolCore для импорта в меню
autopistol_instance = AutoPistolCore()
