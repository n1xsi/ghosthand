import threading
import keyboard
import time
import random


class BhopCore:
    def __init__(self):
        self.running = False  # Глобальный переключатель (вкл/выкл поток)
        self.enabled = False  # Переключатель функционала (для чекбокса в меню)
        self.random_offset = False  # Переключатель случайного смещения прыжка

        self.delay = 0.05     # Задержка между прыжками
        self.is_space_held = False  # Флаг для проверки удержания пробела

    def on_space_press(self, event):
        if not self.is_space_held and self.enabled:
            self.is_space_held = True
            threading.Thread(target=self._loop, daemon=True).start()

    def on_space_release(self, event):
        self.is_space_held = False

    def start(self):
        self.running = True

    def _loop(self):
        while self.is_space_held:
            keyboard.send('space')
            time.sleep(self.delay + (random.uniform(-0.005, 0.005) if self.random_offset else 0))


# Экземпляр класса BhopCore для импорта в меню
bhop_instance = BhopCore()

keyboard.on_press_key('space', bhop_instance.on_space_press)
keyboard.on_release_key('space', bhop_instance.on_space_release)
