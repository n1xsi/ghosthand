from src.core.input_sim import PressKey, ReleaseKey
from src.core.base import ScriptBase
import random
import time


class AntiAfkCore(ScriptBase):
    def __init__(self):
        super().__init__()
        self.action_keys = [0x11, 0x1E, 0x1F, 0x20]  # Scan-коды W, A, S, D

    def _loop(self):
        while self.running:
            if not self.enabled:
                time.sleep(1)
                continue

            key_to_press = random.choice(self.action_keys)
            hold_time = random.uniform(0.1, 0.4)
            wait_time = random.uniform(1.0, 10.0)

            PressKey(key_to_press)
            time.sleep(hold_time)
            ReleaseKey(key_to_press)

            # Дробное ожидание - реагируем на отключение галочки сразу
            elapsed = 0
            while elapsed < wait_time and self.enabled:
                time.sleep(0.1)
                elapsed += 0.1


# Экземпляр класса AntiAfkCore для импорта в меню
antiafk_instance = AntiAfkCore()
