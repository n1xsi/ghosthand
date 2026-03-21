from src.core import input_sim
import threading
import keyboard
import time
import random


class BhopCore:
    def __init__(self):
        self.running = False        # Глобальный переключатель (вкл/выкл поток)
        self.enabled = False        # Переключатель функционала (для чекбокса в меню)
        self.random_offset = False  # Переключатель случайного смещения прыжка

        self.delay = 0.05           # Задержка между прыжками
        self.is_space_held = False  # Флаг для проверки удержания пробела

    def start(self):
        self.running = True
        keyboard.on_press_key('space', self._on_space_press)
        keyboard.on_release_key('space', self._on_space_release)

    def _on_space_press(self, event):
        # Если галочка снята ИЛИ включена Глобальная Пауза - даже не начинаем прыгать
        if not self.is_space_held and self.enabled and not input_sim.GLOBAL_PAUSE:
            self.is_space_held = True
            threading.Thread(target=self._loop, daemon=True).start()

    def _on_space_release(self, event):
        self.is_space_held = False

    def _loop(self):
        while self.is_space_held:
            # Если мы зажали пробел, и ВДРУГ нажали Паузу во время прыжков:
            if input_sim.GLOBAL_PAUSE:
                # Просто ждем в холостую, пока не отпустят пробел или не снимут паузу
                time.sleep(0.01)
                continue

            # Если паузы нет - прыгаем
            keyboard.send('space')
            time.sleep(self.delay + (random.uniform(-0.005, 0.005) if self.random_offset else 0))


# Экземпляр класса BhopCore для импорта в меню
bhop_instance = BhopCore()
