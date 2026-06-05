from src.core.base import ScriptBase
from src.core import input_sim
import threading
import keyboard
import random
import time


class BhopCore(ScriptBase):
    def __init__(self):
        super().__init__()
        self.random_offset = False  # Переключатель случайного смещения прыжка
        self.delay = 0.05           # Задержка между прыжками
        self.is_space_held = False  # Флаг для проверки удержания пробела

    def start(self) -> None:
        """Переопределение start: регистрация хуков вместо запуска _loop."""
        self.running = True
        keyboard.on_press_key('space', self._on_space_press)
        keyboard.on_release_key('space', self._on_space_release)

    def _on_space_press(self, event):
        if not self.is_space_held and self.enabled and not input_sim.GLOBAL_PAUSE:
            self.is_space_held = True
            threading.Thread(target=self._loop, daemon=True).start()

    def _on_space_release(self, event):
        self.is_space_held = False

    def _loop(self):
        while self.is_space_held:
            if input_sim.GLOBAL_PAUSE:
                time.sleep(0.01)
                continue
            offset = random.uniform(-0.005, 0.005) if self.random_offset else 0
            keyboard.send('space')
            time.sleep(self.delay + offset)


# Экземпляр класса BhopCore для импорта в меню
bhop_instance = BhopCore()
