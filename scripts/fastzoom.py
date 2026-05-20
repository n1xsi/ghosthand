from src.core.input_sim import (
    is_key_pressed, MouseClick, ClickKey,
    DIK_Q, VK_MIDBUTTON, MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP,
)
import threading
import time


class FastZoomCore:
    def __init__(self):
        self.running = False
        self.enabled = False

        self.qq_switch = True
        self.macro_delay = 0.015  # Задержка между действиями макроса

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while self.running:
            if not self.enabled:
                time.sleep(0.05)
                continue

            # Если нажата Средняя Кнопка Мыши
            if is_key_pressed(VK_MIDBUTTON):

                # ПКМ (Прицел)
                MouseClick(
                    delay=0.01,
                    m_down=MOUSEEVENTF_RIGHTDOWN,
                    m_up=MOUSEEVENTF_RIGHTUP
                )
                time.sleep(self.macro_delay)

                # ЛКМ (Выстрел)
                MouseClick(delay=0.01)
                time.sleep(self.macro_delay)

                if self.qq_switch:
                    # Нажатие 'Q' (Свап на нож)
                    ClickKey(DIK_Q, delay=0.01)
                    time.sleep(self.macro_delay)

                    # Нажатие 'Q' (Свап обратно на AWP)
                    ClickKey(DIK_Q, delay=0.01)

                # Защита от спама при удержании кнопки
                time.sleep(0.5)
            else:
                time.sleep(0.01)


# Экземпляр класса FastZoomCore для импорта в меню
fastzoom_instance = FastZoomCore()
