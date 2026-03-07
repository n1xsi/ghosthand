import threading
import ctypes
import time


class MiniRecoilCore:
    def __init__(self):
        self.running = False  # Глобальный переключатель (вкл/выкл поток)
        self.enabled = False  # Переключатель функционала (для чекбокса в меню)
        self.strength = 2  # Сила стягивания вниз
        self.speed = 0.01  # Ожидание перед следующим перемещением мыши

        self.left_button_pressed = False  # Флаг для проверки удержания левой кнопки

    def move_mouse(self, dx, dy):
        ctypes.windll.user32.mouse_event(0x0001, dx, dy, 0, 0)

    def mouse_listener(self):
        while True:
            if self.enabled and self.is_left_button_pressed():
                self.left_button_pressed = True
            else:
                self.left_button_pressed = False
            
            if self.left_button_pressed:
                self.move_mouse(0, self.strength)

            time.sleep(self.speed)

    def is_left_button_pressed(self):
        return ctypes.windll.user32.GetAsyncKeyState(0x01) != 0

    def start(self):
        self.running = True
        threading.Thread(target=self.mouse_listener, daemon=True).start()

# Экземпляр класса MiniRecoilCore для импорта в меню
mrc_instance = MiniRecoilCore()
