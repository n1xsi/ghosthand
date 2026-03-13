from src.core.input_sim import POINT, MouseLeftClick, is_key_pressed
import threading
import ctypes
import time

# WinAPI функции для работы с графикой
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32


def get_color(hdc, x, y):
    """Возвращает RGB кортеж пикселя по координатам"""
    # GetPixel возвращает цвет в формате 0x00BBGGRR
    color = gdi32.GetPixel(hdc, x, y)

    # Битовые сдвиги для получения чистого R, G, B
    r = color & 0xFF
    g = (color >> 8) & 0xFF
    b = (color >> 16) & 0xFF
    return r, g, b


class TriggerBotCore:
    def __init__(self):
        self.running = False
        self.enabled = False

        self.threshold = 20  # Допуск изменения цвета
        self.reaction_delay = 0.01  # Задержка перед выстрелом
        self.shoot_delay = 0.15  # Задержка между выстрелами

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        was_pressed = False
        ref_r, ref_g, ref_b = 0, 0, 0
        hdc = None
        pt = POINT()

        while self.running:
            if not self.enabled:
                time.sleep(0.1)
                continue

            # Проверка, зажат ли триггер (Левый ALT)
            if is_key_pressed(0xA4):

                # ПЕРВОЕ НАЖАТИЕ (Захват начального цвета)
                if not was_pressed:
                    # Получение контекста всего экрана (0)
                    hdc = user32.GetDC(0)
                    user32.GetCursorPos(ctypes.byref(pt))

                    # Берётся цвет с отступом +2 пикселя
                    # Отступ нужен, чтобы не захватить цвет самого прицела игры
                    ref_r, ref_g, ref_b = get_color(hdc, pt.x + 2, pt.y + 2)
                    was_pressed = True

                # УДЕРЖАНИЕ (Сравнение цветов)
                else:
                    curr_r, curr_g, curr_b = get_color(hdc, pt.x + 2, pt.y + 2)

                    # Вычисление математического расстояния между двумя цветами (Евклидова метрика)
                    # Это (по идее) должно решать проблему с тёмными цветами
                    color_distance = (
                        (curr_r - ref_r)**2 +
                        (curr_g - ref_g)**2 +
                        (curr_b - ref_b)**2
                    )**0.5

                    # Динамическая корректировка: если базовый цвет очень тёмный,
                    # то делаем триггер более чувствительным (уменьшение порога в 2 раза)
                    current_threshold = self.threshold
                    # Сумма RGB < 100 значит, что мы смотрим в темноту
                    if (ref_r + ref_g + ref_b) < 100:
                        current_threshold = self.threshold * 0.5

                    # Если дистанция цвета больше порога - SHOOT!
                    if color_distance > current_threshold:
                        time.sleep(self.reaction_delay)  # Задержка перед выстрелом
                        MouseLeftClick(delay=0.01)  # Зажатие левой кнопки мыши в течение 0.01 сек

                        # Ожидание перед следующим кликом, чтобы не спамить
                        time.sleep(self.shoot_delay)

                        # После выстрела обновление базового цвета (опционально, но по идее помогает при отдаче)
                        user32.GetCursorPos(ctypes.byref(pt))
                        ref_r, ref_g, ref_b = get_color(hdc, pt.x + 2, pt.y + 2)

            # КЛАВИША ОТПУЩЕНА
            else:
                if was_pressed:
                    # Освобождение памяти видеокарты (memory leak protection)
                    user32.ReleaseDC(0, hdc)
                    was_pressed = False
                time.sleep(0.005)


# Экземпляр класса TriggerBotCore для импорта в меню
pixel_trigger_instance = TriggerBotCore()
