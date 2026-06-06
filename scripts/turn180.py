from src.core.input_sim import MouseMove, is_key_pressed, VK_T
from src.core.base import ScriptBase
import time


class Turn180Core(ScriptBase):
    def __init__(self):
        super().__init__()

        self.pixels = 3200  # Подбирается ползунком под конкретную сенсу
        self.steps = 10     # Количество микро-шагов (для плавности)

    def _loop(self):
        was_pressed = False

        while self.running:
            if not self.enabled:
                time.sleep(0.1)
                continue

            current_state = is_key_pressed(VK_T)

            # Если кнопку ТОЛЬКО ЧТО нажали
            if current_state and not was_pressed:
                was_pressed = True
                step_pixels = int(self.pixels / self.steps)
                for _ in range(self.steps):
                    MouseMove(step_pixels, 0)
                    # Микро-пауза между смещениями (имитация рывка руки)
                    time.sleep(0.002)
                time.sleep(0.2)  # Кулдаун после разворота
            elif not current_state:
                was_pressed = False

            time.sleep(0.01)


turn180_instance = Turn180Core()
