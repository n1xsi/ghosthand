from src.core.input_sim import POINT, MouseClick, is_key_pressed, user32, DIK_ALT
from src.core.base import ScriptBase
import ctypes
import time

gdi32 = ctypes.windll.gdi32  # WinAPI для работы с графикой


def _get_pixel(hdc, x: int, y: int) -> tuple[int, int, int]:
    """Возвращает (R, G, B) пикселя по экранным координатам."""
    color = gdi32.GetPixel(hdc, x, y)  # 0x00BBGGRR
    return color & 0xFF, (color >> 8) & 0xFF, (color >> 16) & 0xFF


class TriggerBotCore(ScriptBase):
    def __init__(self):
        super().__init__()

        self.threshold = 20  # Допуск изменения цвета
        self.reaction_delay = 0.01  # Задержка перед выстрелом
        self.shoot_delay = 0.15  # Задержка между выстрелами

    def _loop(self):
        was_pressed = False
        ref_r, ref_g, ref_b = 0, 0, 0
        hdc = None
        pt = POINT()

        while self.running:
            if not self.enabled:
                time.sleep(0.1)
                continue

            if is_key_pressed(DIK_ALT):

                # ПЕРВОЕ НАЖАТИЕ (Захват начального цвета)
                if not was_pressed:
                    # Получение контекста всего экрана (0)
                    hdc = user32.GetDC(0)
                    user32.GetCursorPos(ctypes.byref(pt))

                    # Берётся цвет с отступом +2 пикселя
                    # Отступ нужен, чтобы не захватить цвет самого прицела игры
                    ref_r, ref_g, ref_b = _get_pixel(hdc, pt.x + 2, pt.y + 2)
                    was_pressed = True

                # УДЕРЖАНИЕ (Сравнение цветов)
                else:
                    curr_r, curr_g, curr_b = _get_pixel(hdc, pt.x + 2, pt.y + 2)

                    # Вычисление математического расстояния между двумя цветами (Евклидова метрика)
                    color_distance = (
                        (curr_r - ref_r)**2 +
                        (curr_g - ref_g)**2 +
                        (curr_b - ref_b)**2
                    )**0.5

                    # Тёмный фон → делаем триггер чувствительнее
                    threshold = self.threshold * (0.5 if (ref_r + ref_g + ref_b) < 100 else 1.0)

                    # Если дистанция цвета больше порога - SHOOT!
                    if color_distance > threshold:
                        # Задержка перед выстрелом
                        time.sleep(self.reaction_delay)
                        # Зажатие левой кнопки мыши в течение 0.01 сек
                        MouseClick(delay=0.01)
                        # Ожидание перед следующим кликом, чтобы не спамить
                        time.sleep(self.shoot_delay)

                        # Обновляем опорный цвет после выстрела (компенсация отдачи)
                        user32.GetCursorPos(ctypes.byref(pt))
                        ref_r, ref_g, ref_b = _get_pixel(hdc, pt.x + 2, pt.y + 2)

            # КЛАВИША ОТПУЩЕНА
            else:
                if was_pressed:
                    user32.ReleaseDC(0, hdc)  # Освобождаем HDC (предотвращение memory leak)
                    was_pressed = False
                time.sleep(0.005)


# Экземпляр класса TriggerBotCore для импорта в меню
pixel_trigger_instance = TriggerBotCore()
