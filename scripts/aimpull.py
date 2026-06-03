from src.core.input_sim import MouseMove, is_key_pressed, VK_LBUTTON
from src.core.base import ScriptBase
import numpy as np
import time
import math
import mss


class AimPullCore(ScriptBase):
    def __init__(self):
        super().__init__()

        self.smooth = 1.0    # Делитель скорости (больше = медленнее доводка)
        self.fov = 100       # Размер квадрата поиска (пикселей от центра)
        self.tolerance = 60  # Допуск изменения цвета

        # Цвет цели: R=216, G=42, B=34 (0xD82A22). Формат MSS: BGR
        self.target_color = np.array([34, 42, 216])

        # Переменные для отображения круга (FOV)
        self.show_fov = False         # Показывать ли круг
        self.fov_color = "#FFFFFF"  # Цвет круга (по умолчанию белый)

    def _loop(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            center_x = monitor["width"] // 2
            center_y = monitor["height"] // 2

            while self.running:
                if not self.enabled:
                    time.sleep(0.1)
                    continue

                if not is_key_pressed(VK_LBUTTON):
                    time.sleep(0.005)
                    continue

                # Зона поиска (квадрат вокруг прицела)
                bbox = {
                    "top": center_y - self.fov,
                    "left": center_x - self.fov,
                    "width": self.fov * 2,
                    "height": self.fov * 2
                }

                # Скриншот зоны + удаление альфа-канала
                pixels = np.array(sct.grab(bbox))[:, :, :3]

                # Поиск пикселя нужного цвета с учетом tolerance
                diff = np.abs(pixels - self.target_color)
                mask = np.all(diff <= self.tolerance, axis=-1)

                # Получение координат всех найденных пикселей: (y, x)
                found_pixels = np.argwhere(mask)

                if not len(found_pixels):
                    time.sleep(0.005)
                    continue

                # Берётся первый попавшийся пиксель
                target_y_local, target_x_local = found_pixels[0]

                # Перевод локальных координат в экранные относительно прицела
                AimX = target_x_local - self.fov
                AimY = target_y_local - self.fov

                # Deadzone - не трясёмся если уже на цели
                if abs(AimX) < 3 and abs(AimY) < 3:
                    time.sleep(0.005)
                    continue

                # Направление
                DirX = 1 if AimX > 0 else -1
                DirY = 1 if AimY > 0 else -1

                # Формула доводки
                MoveX = math.sqrt(abs(AimX)) * DirX
                MoveY = math.sqrt(abs(AimY)) * DirY

                MouseMove(
                    int((MoveX * 1.5) / self.smooth),
                    int(MoveY / self.smooth),
                )

                # Задержка
                time.sleep(0.01)


# Экземпляр класса AimPullCore для импорта в меню
aimpull_instance = AimPullCore()
