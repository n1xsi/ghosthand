from src.core.input_sim import MouseMove, is_key_pressed, VK_LBUTTON
from src.core.base import ScriptBase
import time


class MiniRecoilCore(ScriptBase):
    def __init__(self):
        super().__init__()
        self.strength = 2  # Сила стягивания вниз (пикселей)
        self.speed = 0.01  # Задержка между перемещениями

    def _loop(self):
        while self.running:
            if self.enabled and is_key_pressed(VK_LBUTTON):
                MouseMove(0, self.strength)
                time.sleep(self.speed)
            else:
                time.sleep(0.01)


# Экземпляр класса MiniRecoilCore для импорта в меню
mrc_instance = MiniRecoilCore()
