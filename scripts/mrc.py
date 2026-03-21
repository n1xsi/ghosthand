from src.core.input_sim import MouseMove, is_key_pressed, VK_LBUTTON
import threading
import time


class MiniRecoilCore:
    def __init__(self):
        self.running = False  # Глобальный переключатель (вкл/выкл поток)
        self.enabled = False  # Переключатель функционала (для чекбокса в меню)
        self.strength = 2  # Сила стягивания вниз
        self.speed = 0.01  # Ожидание перед следующим перемещением мыши

    def _loop(self):
        while self.running:
            if self.enabled and is_key_pressed(VK_LBUTTON):
                MouseMove(0, self.strength)
                time.sleep(self.speed)
            else:
                # Если не стреляем - не грузим процессор
                time.sleep(0.01)

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()


# Экземпляр класса MiniRecoilCore для импорта в меню
mrc_instance = MiniRecoilCore()
