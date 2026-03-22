from src.core.input_sim import MouseLeftClick, is_key_pressed, VK_XBUTTON1
import threading
import time


class AutoPistolCore:
    def __init__(self):
        self.running = False  # Глобальный переключатель потока
        self.enabled = False  # Переключатель функционала (чекбокс в меню)
        self.delay = 0.01     # Задержка между выстрелами

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while self.running:
            # Если галочка стоит и боковая кнопка зажата
            if self.enabled and is_key_pressed(VK_XBUTTON1):
                MouseLeftClick(delay=0.01)
                time.sleep(self.delay)
            else:
                time.sleep(0.01)


# Экземпляр класса AutoPistolCore для импорта в меню
autopistol_instance = AutoPistolCore()
