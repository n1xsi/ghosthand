import threading
import time

import dearpygui.dearpygui as dpg

from src.core import input_sim


class PanicCore:
    """
    Panic key (глобальная пауза) — слушает 'PAUSE/Break' и переключает input_sim.GLOBAL_PAUSE.

    Использует GetAsyncKeyState напрямую (не через is_key_pressed),
    чтобы сама пауза не блокировала чтение своей же кнопки.
    """

    def start(self) -> None:
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self) -> None:
        was_pressed = False

        while True:
            current = (input_sim.user32.GetAsyncKeyState(input_sim.VK_PAUSE) & 0x8000) != 0

            if current and not was_pressed:
                input_sim.GLOBAL_PAUSE = not input_sim.GLOBAL_PAUSE
                was_pressed = True
                self._update_ui(input_sim.GLOBAL_PAUSE)

            elif not current:
                was_pressed = False

            time.sleep(0.01)

    @staticmethod
    def _update_ui(paused: bool) -> None:
        try:
            if paused:
                dpg.set_value("status_text", "GLOBAL PAUSE")
                dpg.configure_item("status_text", color=(255, 50, 50, 255))
                print("[debug:panic] GLOBAL PAUSE")
            else:
                dpg.set_value("status_text", "SYSTEM ACTIVE")
                dpg.configure_item("status_text", color=(50, 255, 50, 255))
                print("[debug:panic] SYSTEM ACTIVE")
        except Exception:
            pass  # DPG может быть ещё не инициализирован


# Экземпляр класса PanicCore для импорта в меню
panic_instance = PanicCore()
