from src.core.input_sim import MouseMove, is_key_pressed
import threading
import time

VK_F = 0x46  # Виртуальный код клавиши 'F'

class AntiAimCore:
    def __init__(self):
        self.running = False
        self.enabled = False  # Разрешено ли использовать функцию (Галочка в меню)
        self.active = False  # Включить ли антиаимы (Клавиша F)

        # Настройки из меню
        self.frequency = 0.15  # Как часто дергается голова (секунды)
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

            current_key_state = is_key_pressed(VK_F)  # Проверка нажатия клавиши F
            # Если клавиша ТОЛЬКО ЧТО нажата (ранее была отпущена)
            if current_key_state and not key_was_pressed:
                self.active = not self.active  # Переключаем состояние (True -> False -> True)
                print(f"[Core] Anti-Aim Togged: {'ON' if self.active else 'OFF'}")
                key_was_pressed = True

            # Если клавишу отпустили - сбрасываем флаг
            elif not current_key_state:
                key_was_pressed = False

            if self.active:
                # Рассчитывание вектора сдвига:
                # По оси Y берётся 1/3 от X (4500 и 1500), чтобы персонаж смотрел по диагонали вниз.
                dx, dy = int(self.strength), int(self.strength // 3)

                # РЫВОК
                MouseMove(dx, dy)

                # Ожидание 15 миллисекунд
                # Это время нужно игровому движку, чтобы зарегистрировать "сломанный" угол на сервере
                time.sleep(0.015)

                # ВОЗВРАТ (Возвращение прицела на место)
                MouseMove(-dx, -dy)

                # Ожидание до следующего тика (Настройка частоты)
                time.sleep(self.frequency)
            else:
                # Если функция разрешена (галочка стоит), но выключена клавишей F
                # Спим чуть-чуть, чтобы быстро среагировать на нажатие F
                time.sleep(0.005)

# Экземпляр класса BhopCore для импорта в меню
anti_aim_instance = AntiAimCore()
