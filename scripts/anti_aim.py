from src.core.input_sim import MouseMove, is_key_pressed, VK_F
from src.core.base import ScriptBase
import time


class AntiAimCore(ScriptBase):
    def __init__(self):
        super().__init__()

        self.active = False    # Переключение клавишей F
        self.frequency = 0.15  # Частота рывков головы (секунды)
        self.strength = 4500   # Угол/Сила рывка (пикселей мыши)

    def _loop(self):
        key_was_pressed = False

        while self.running:
            if not self.enabled:
                time.sleep(0.1)
                continue

            current_key_state = is_key_pressed(VK_F)

            # Если клавиша ТОЛЬКО ЧТО нажата (ранее была отпущена)
            if current_key_state and not key_was_pressed:
                self.active = not self.active
                print(f"[Core] Anti-Aim Togged: {'ON' if self.active else 'OFF'}")
                key_was_pressed = True

            # Если клавишу отпустили - сброс флага
            elif not current_key_state:
                key_was_pressed = False

            if self.active:
                # Y = 1/3 от X → диагональный рывок вниз
                dx, dy = int(self.strength), int(self.strength // 3)
                # РЫВОК
                MouseMove(dx, dy)
                # Время для регистрации угла на сервере
                time.sleep(0.015)
                # ВОЗВРАТ (прицела на место)
                MouseMove(-dx, -dy)
                # Ожидание до следующего тика
                time.sleep(self.frequency)
            else:
                # Если функция разрешена (галочка стоит), но выключена клавишей F
                time.sleep(0.005)


# Экземпляр класса AntiAimCore для импорта в меню
anti_aim_instance = AntiAimCore()
