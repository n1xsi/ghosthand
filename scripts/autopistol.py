from src.core.input_sim import MouseClick, is_key_pressed, VK_XBUTTON1
from src.core.base import ScriptBase
import time


class AutoPistolCore(ScriptBase):
    def __init__(self):
        super().__init__()
        self.delay = 0.01  # Задержка между выстрелами

    def _loop(self):
        while self.running:
            if self.enabled and is_key_pressed(VK_XBUTTON1):
                MouseClick(delay=0.01)
                time.sleep(self.delay)
            else:
                time.sleep(0.01)


# Экземпляр класса AutoPistolCore для импорта в меню
autopistol_instance = AutoPistolCore()
