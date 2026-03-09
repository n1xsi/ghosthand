import threading
import keyboard
import time
import random


class AntiAfkCore:
    def __init__(self):
        self.running = False  # Глобальный переключатель (вкл/выкл поток)
        self.enabled = False  # Переключатель функционала (для чекбокса в меню)

        self.action_keys = [0x11, 0x1E, 0x1F, 0x20]  # Клавиши нажатия для имитации действий (WASD)

    def _loop(self):
        while self.running:
            if not self.enabled:
                time.sleep(1)  # Если выключено - то долгое ожидание, чтобы не грузить CPU
                continue

            key_to_press = random.choice(self.action_keys)
            hold_time = random.uniform(0.1, 0.4)
            wait_time = random.uniform(1.0, 10.0)

            keyboard.press(key_to_press)
            time.sleep(hold_time)
            keyboard.release(key_to_press)
            time.sleep(wait_time)

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()


# Экземпляр класса AntiAfkCore для импорта в меню
antiafk_instance = AntiAfkCore()
