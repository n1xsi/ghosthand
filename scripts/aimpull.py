from src.core.input_sim import MouseMove, is_key_pressed
import time
import threading
import math
import mss
import numpy as np

# VK код для Левой Кнопки Мыши
VK_LBUTTON = 0x01


class AimPullCore:
    def __init__(self):
        self.running = False
        self.enabled = False

        # Делитель скорости (Больше = медленнее доводка)
        self.smooth = 1.0
        # Размер квадрата поиска (100x100 пикселей от центра)
        self.fov = 100
        self.tolerance = 60  # Допуск изменения цвета (аналог ColVn из AHK)

        # Цвет: Red: 216, Green: 42, Blue: 34 (0xD82A22 из AHK)
        # В OpenCV и MSS формат цвета B, G, R!!!
        self.target_color = np.array([34, 42, 216])

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        print("[Core] AimPull Loaded. AHK Sqrt-Algorithm active.")
        
        # Инициализация mss ВНУТРИ потока
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Получение разрешение основного монитора
            center_x = monitor["width"] // 2
            center_y = monitor["height"] // 2

            while self.running:
                if not self.enabled:
                    time.sleep(0.1)
                    continue

                # Триггер: Зажата ли Левая Кнопка Мыши?
                if is_key_pressed(VK_LBUTTON):
                    
                    # Зона поиска (Квадрат вокруг прицела)
                    bbox = {
                        "top": center_y - self.fov,
                        "left": center_x - self.fov,
                        "width": self.fov * 2,
                        "height": self.fov * 2
                    }

                    # Делается скриншот зоны
                    img = np.array(sct.grab(bbox))
                    
                    # Удаление Альфа-канала (он нам не нужен), оставляем BGR
                    pixels = img[:, :, :3]

                    # Поиск пикселя нужного цвета с учетом tolerance
                    diff = np.abs(pixels - self.target_color)
                    mask = np.all(diff <= self.tolerance, axis=-1)
                    
                    # Получение координат всех найденных пикселей: (y, x)
                    found_pixels = np.argwhere(mask)

                    if len(found_pixels) > 0:
                        # Берётся первый попавшийся пиксель
                        target_y_local, target_x_local = found_pixels[0]
                        
                        # Локальные координаты переводятся в экранные относительно прицела
                        AimX = target_x_local - self.fov
                        AimY = target_y_local - self.fov

                        # Deadzone (чтобы прицел не трясся, если он уже на цели)
                        if abs(AimX) < 3 and abs(AimY) < 3:
                            time.sleep(0.005)
                            continue

                        # Направление
                        DirX = 1 if AimX > 0 else -1
                        DirY = 1 if AimY > 0 else -1

                        # ФОРМУЛА ДОВОДКИ
                        MoveX = math.sqrt(abs(AimX)) * DirX
                        MoveY = math.sqrt(abs(AimY)) * DirY

                        FinalX = int((MoveX * 1.5) / self.smooth)
                        FinalY = int(MoveY / self.smooth)

                        # Перемещение мыши
                        MouseMove(FinalX, FinalY)
                        
                        # Задержка
                        time.sleep(0.01)
                else:
                    # Если ЛКМ не зажата
                    time.sleep(0.005)

# Экземпляр класса AimPullCore для импорта в меню
aimpull_instance = AimPullCore()
