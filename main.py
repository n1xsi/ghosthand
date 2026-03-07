from scripts.bunnyhop import bhop_instance
import dearpygui.dearpygui as dpg

# Функции обратного вызова (Callbacks)
def toggle_bhop(sender, app_data):
    bhop_instance.enabled = app_data  # app_data содержит True/False от чекбокса
    status = "ON" if app_data else "OFF"
    print(f"[bhop] {status}")


def change_delay(sender, app_data):
    bhop_instance.delay = app_data  # app_data содержит float от слайдера
    print(f"Delay set to {app_data}")


def toggle_random_offset(sender, app_data):
    bhop_instance.random_offset = app_data  # app_data содержит True/False от чекбокса
    status = "ON" if app_data else "OFF"
    print(f"[random_offset] {status}")


# Инициализация GUI
dpg.create_context()
dpg.create_viewport(title='Ghosthand v0.1', width=400, height=300)
dpg.setup_dearpygui()

with dpg.window(label="Main Menu", width=400, height=300, no_collapse=True, no_move=True):
    dpg.add_text("GHOSTHAND ACTIVATED", color=(0, 255, 0))
    dpg.add_separator()

    dpg.add_text("Modules:")

    # Чекбокс, который меняет self.enabled в логике
    dpg.add_checkbox(label="Enable Bunnyhop", callback=toggle_bhop)

    # Слайдер задержки
    dpg.add_slider_float(label="Jump Delay (sec)", default_value=bhop_instance.delay,
                         min_value=0.005, max_value=0.1, callback=change_delay)

    # Чекбокс рандомного смещения прыжка
    dpg.add_checkbox(label="Randomize Jump Offset",
                     callback=toggle_random_offset)

    dpg.add_spacer(height=20)
    dpg.add_text("Hold SPACE to activate in-game", color=(150, 150, 150))

# Запуск скриптов
bhop_instance.start()  # Запуск потока с бхопом перед отрисовкой окна

# Запуск цикла отрисовки
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
