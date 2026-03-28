from src.core.input_sim import MouseMove, is_key_pressed, VK_T
import threading
import time


class Turn180Core:
    def __init__(self):
        self.running = False
        self.enabled = False

        # Дефолтное значение из твоего AHK-скрипта (примерно 3200 пикселей при sens=1)
        # Это значение пользователь будет подгонять ползунком в меню
        self.pixels = 3200

        # На сколько кусков разбить движение (для плавности и обхода античита)
        self.steps = 10

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        # Флаг, чтобы скрипт не крутил тебя как спиннер, если ты зажал кнопку
        was_pressed = False

        while self.running:
            if not self.enabled:
                time.sleep(0.1)
                continue

            current_state = is_key_pressed(VK_T)

            # Если кнопку ТОЛЬКО ЧТО нажали
            if current_state and not was_pressed:
                was_pressed = True

                # Считаем, сколько пикселей двигать за один микро-шаг
                step_pixels = int(self.pixels / self.steps)

                # Выполняем поворот
                for _ in range(self.steps):
                    MouseMove(step_pixels, 0)
                    # Микро-пауза между смещениями (имитация рывка руки)
                    time.sleep(0.002)

                # Небольшой кулдаун после разворота
                time.sleep(0.2)

            elif not current_state:
                was_pressed = False

            time.sleep(0.01)


turn180_instance = Turn180Core()
