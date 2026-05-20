from src.core.input_sim import MouseMove, is_key_pressed, VK_F
import threading
import time


class AntiAimCore:
    def __init__(self):
        self.running = False
        self.enabled = False  # Галочка в меню
        self.active = False   # Переключение клавишей F

        self.frequency = 0.15  # Как часто дёргается голова (секунды)
        self.strength = 4500   # Угол/Сила рывка (в пикселях мыши)

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

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
                # Рассчитывание вектора сдвига:
                # Y = 1/3 от X => персонаж смотрит по диагонали вниз
                dx, dy = int(self.strength), int(self.strength // 3)

                # РЫВОК
                MouseMove(dx, dy)

                # Ожидание 15 миллисекунд
                # Время, чтобы движок зарегистрировал сломанный угол
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
