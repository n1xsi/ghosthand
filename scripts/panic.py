from src.core import input_sim
import dearpygui.dearpygui as dpg
import threading
import time


VK_PAUSE = 0x13 # Кнопка Pause/Break

def panic_loop():
    was_pressed = False

    while True:
        # Чтение кнопки НАПРЯМУЮ через Windows, иначе пауза заблокирует чтение кнопки Паузы ))
        current_state = (input_sim.user32.GetAsyncKeyState(VK_PAUSE) & 0x8000) != 0

        if current_state and not was_pressed:
            # Переключение глобальной переменной в ядре
            input_sim.GLOBAL_PAUSE = not input_sim.GLOBAL_PAUSE
            was_pressed = True

            # Смена цвета текста в меню
            try:
                if input_sim.GLOBAL_PAUSE:
                    dpg.set_value("status_text", "GLOBAL PAUSE")
                    dpg.configure_item("status_text", color=(255, 50, 50, 255))
                else:
                    dpg.set_value("status_text", "SYSTEM ACTIVE")
                    dpg.configure_item("status_text", color=(50, 255, 50, 255))
            except: pass

        elif not current_state:
            was_pressed = False

        time.sleep(0.01)

# Автоматический запуск потока при импорте этого файла
threading.Thread(target=panic_loop, daemon=True).start()
