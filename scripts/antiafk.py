from src.core.input_sim import PressKey, ReleaseKey
import threading
import time
import random


class AntiAfkCore:
    def __init__(self):
        self.running = False  # Глобальный переключатель (вкл/выкл поток)
        self.enabled = False  # Переключатель функционала (для чекбокса в меню)

        # Клавиши нажатия для имитации действий (W, A, S, D)
        self.action_keys = [0x11, 0x1E, 0x1F, 0x20]

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while self.running:
            if not self.enabled:
                # Если выключено - то долгое ожидание, чтобы не грузить CPU
                time.sleep(1)
                continue

            key_to_press = random.choice(self.action_keys)
            hold_time = random.uniform(0.1, 0.4)
            wait_time = random.uniform(1.0, 10.0)

            PressKey(key_to_press)
            time.sleep(hold_time)
            ReleaseKey(key_to_press)

            # "Умное" ожидание, чтобы реагировать на отключение галочки мгновенно
            elapsed = 0
            while elapsed < wait_time and self.enabled:
                time.sleep(0.1)
                elapsed += 0.1


# Экземпляр класса AntiAfkCore для импорта в меню
antiafk_instance = AntiAfkCore()
