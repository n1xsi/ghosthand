from scripts.bunnyhop import bhop_instance
from scripts.mrc import mrc_instance
import dearpygui.dearpygui as dpg

# -------------------------- CALLBACKS --------------------------

# ----- bhop -----
def toggle_bhop(sender, app_data):
    """
    sender: кто вызвал функцию (чекбокс)
    app_data: значение чекбокса (True/False)
    """
    bhop_instance.enabled = app_data
    dpg.configure_item("bhop_settings_group", show=app_data)
    status = "ON" if app_data else "OFF"
    print(f"[debug-UI] bhop is {status}")


def update_bhop_delay(sender, app_data):
    bhop_instance.delay = app_data
    print(f"[debug-UI] bhop delay set to {app_data:.4f}s")


def toggle_random_offset(sender, app_data):
    bhop_instance.random_offset = app_data
    status = "ON" if app_data else "OFF"
    print(f"[debug-UI] bhop random offset is {status}")

# ----- mrc -----
def toggle_mrc(sender, app_data):
    mrc_instance.enabled = app_data
    status = "ON" if app_data else "OFF"
    print(f"[debug-UI] mrc is {status}")


# -------------------------- GUI SETUP --------------------------
dpg.create_context()  # Инициализация DearPyGui

with dpg.window(tag="Primary Window", width=500, height=350, no_resize=True, no_move=True, no_collapse=True, no_title_bar=True):
    
    # Заголовок
    with dpg.group(horizontal=True):
        dpg.add_text("GHOSTHAND", color=(139, 0, 255, 255))
        dpg.add_text("v0.2 | Dev Build", color=(150, 150, 150, 200))
    
    dpg.add_separator()
    dpg.add_spacer(height=5)

    # ----- ВКЛАДКИ -----
    with dpg.tab_bar():
        
        # Вкладка 1: Aim Assist
        with dpg.tab(label="Aim Assist"):
            dpg.add_spacer(height=10)
            dpg.add_checkbox(label="AimPull", enabled=False)
            dpg.add_checkbox(label="Smooth", enabled=False)
            dpg.add_checkbox(label="Pixel Trigger Bot", enabled=False)
            dpg.add_checkbox(label="AutoPistol", enabled=False)
            dpg.add_checkbox(label="Mini-Recoil Control", callback=toggle_mrc)
            # FIXME: add slider for "Mini-Recoil Control" strength

        # Вкладка 2: Anti-Aim
        with dpg.tab(label="Anti-Aim"):
            dpg.add_spacer(height=10)
            dpg.add_checkbox(label="Enable", enabled=False)

        # Вкладка 3: Movement
        with dpg.tab(label="Movement"):
            dpg.add_spacer(height=10)
            dpg.add_checkbox(label="Bhop", callback=toggle_bhop)

            with dpg.group(tag="bhop_settings_group", show=False):
                dpg.add_spacer(height=5)

                # Рамка вокруг настроек (Child Window) для красоты
                with dpg.child_window(height=105, border=True):
                    dpg.add_text("Bhop Settings", color=(163, 102, 255))
                    dpg.add_checkbox(label="Randomize Jump Offset", callback=toggle_random_offset)
                    dpg.add_slider_float(
                        label="Jump Delay (sec)",
                        default_value=bhop_instance.delay,
                        min_value=0.005,
                        max_value=0.1,
                        callback=update_bhop_delay,
                        format="%.3f"
                    )
                    dpg.add_text("Lower delay = Faster spam. Hold SPACE to activate in-game.", color=(150, 150, 150))

            dpg.add_checkbox(label="Anti-AFK", enabled=False)
            dpg.add_checkbox(label="Snap Tap", enabled=False)

        # Вкладка 4: Misc
        with dpg.tab(label="Misc"):
            dpg.add_spacer(height=10)
            dpg.add_checkbox(label="Secured Mode", enabled=False)
            dpg.add_checkbox(label="Fast-Zoom", enabled=False)
            dpg.add_checkbox(label="Zoom to Mouse", enabled=False)
            dpg.add_button(label="PANIC UNLOAD", width=120)
            # configs system
            # theme system

        # Вкладка 5: Keybinds
        with dpg.tab(label="Keybinds"):
            dpg.add_spacer(height=10)
            dpg.add_text("Menu Key: INSERT")
            dpg.add_text("Panic Key: DELETE")


# -------------------------- ЗАПУСК --------------------------
dpg.create_viewport(title='ghosthand', width=515, height=390, resizable=False, decorated=True)
dpg.setup_dearpygui()

# ----- Запуск скриптов -----
bhop_instance.start()
mrc_instance.start()

dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
