from scripts.pixel_triggerbot import pixel_trigger_instance
from scripts.autopistol import autopistol_instance
from scripts.anti_aim import anti_aim_instance
from scripts.fastzoom import fastzoom_instance
from scripts.snaptap import snap_tap_instance
from scripts.antiafk import antiafk_instance
from scripts.aimpull import aimpull_instance
from scripts.bunnyhop import bhop_instance
from scripts.mrc import mrc_instance
import scripts.panic

import dearpygui.dearpygui as dpg


# Переменные цветов
DEEP_PURPLE = (139, 0, 255, 255)
SOFT_PURPLE = (163, 102, 255, 255)
ACTIVE_PURPLE = (184, 102, 255, 255)
ADDITIONAL_BLACK = (150, 150, 150, 200)

# -------------------------- CALLBACKS --------------------------

# ----- aimpull -----
def toggle_aimpull(sender, app_data):
    aimpull_instance.enabled = app_data
    dpg.configure_item("aimpull_settings_group", show=app_data)
    print(f"[debug-UI] AimPull is {"ON" if app_data else "OFF"}")


def update_smooth(sender, app_data):
    aimpull_instance.smooth = app_data
    print(f"[debug-UI] AimPull smooth set to {app_data:.1f}")


def update_fov(sender, app_data):
    aimpull_instance.fov = app_data
    print(f"[debug-UI] AimPull FOV set to {app_data}")

# ----- autopistol -----
def toggle_autopistol(sender, app_data):
    autopistol_instance.enabled = app_data
    dpg.configure_item("autopistol_settings_group", show=app_data)
    print(f"[debug-UI] autopistol is {"ON" if app_data else "OFF"}")


def update_autopistol_delay(sender, app_data):
    autopistol_instance.delay = app_data
    print(f"[debug-UI] autopistol delay set to {app_data:.4f}s")

# ----- trigger -----
def toggle_pixel_trigger(sender, app_data):
    pixel_trigger_instance.enabled = app_data
    dpg.configure_item("trigger_settings_group", show=app_data)
    print(f"[debug-UI] trigger is {"ON" if app_data else "OFF"}")


def update_pixel_trigger_reaction_delay(sender, app_data):
    pixel_trigger_instance.reaction_delay = app_data
    print(f"[debug-UI] pixel trigger reaction delay set to {app_data:.4f}s")


def update_pixel_trigger_threshold(sender, app_data):
    pixel_trigger_instance.threshold = app_data
    print(f"[debug-UI] pixel trigger threshold set to {app_data}")

# ----- mrc -----
def toggle_mrc(sender, app_data):
    mrc_instance.enabled = app_data
    dpg.configure_item("mrc_settings_group", show=app_data)
    print(f"[debug-UI] mrc is {"ON" if app_data else "OFF"}")


def update_mrc_strength(sender, app_data):
    mrc_instance.strength = app_data
    print(f"[debug-UI] mrc strength set to {app_data:.4f}")


def update_mrc_speed(sender, app_data):
    mrc_instance.speed = app_data
    print(f"[debug-UI] mrc speed set to {app_data:.4f}")

# ----- anti-aim -----
def toggle_aa(sender, app_data):
    anti_aim_instance.enabled = app_data
    dpg.configure_item("antiaim_settings_group", show=app_data)
    print(f"[debug-UI] Anti-Aim is {"ON" if app_data else "OFF"}")


def update_aa_frequency(sender, app_data):
    anti_aim_instance.frequency = app_data


def update_aa_strength(sender, app_data):
    anti_aim_instance.strength = app_data

# ----- bhop -----
def toggle_bhop(sender, app_data):
    bhop_instance.enabled = app_data
    dpg.configure_item("bhop_settings_group", show=app_data)
    print(f"[debug-UI] bhop is {"ON" if app_data else "OFF"}")


def update_bhop_delay(sender, app_data):
    bhop_instance.delay = app_data
    print(f"[debug-UI] bhop delay set to {app_data:.4f}s")


def toggle_random_offset(sender, app_data):
    bhop_instance.random_offset = app_data
    print(f"[debug-UI] bhop random offset is {"ON" if app_data else "OFF"}")

# ----- snap tap -----
def toggle_snap_tap(sender, app_data):
    snap_tap_instance.enabled = app_data
    print(f"[debug-UI] snap tap is {"ON" if app_data else "OFF"}")

# ----- anti-afk -----
def toggle_antiafk(sender, app_data):
    antiafk_instance.enabled = app_data
    print(f"[debug-UI] anti-afk is {"ON" if app_data else "OFF"}")

# ----- fast zoom -----
def toggle_fastzoom(sender, app_data):
    fastzoom_instance.enabled = app_data
    print(f"[debug-UI] Fast-Zoom is {"ON" if app_data else "OFF"}")


# -------------------------- GUI SETUP --------------------------
dpg.create_context()  # Инициализация DearPyGui

with dpg.window(tag="Primary Window", width=680, height=480, no_resize=True, no_move=True, no_collapse=True, no_title_bar=True):

    # Заголовок
    with dpg.group(horizontal=True):
        dpg.add_text("GHOSTHAND", color=DEEP_PURPLE)
        dpg.add_text("v0.8 | Dev Build", color=ADDITIONAL_BLACK)
        dpg.add_text("SYSTEM ACTIVE", tag="status_text", color=(50, 255, 50, 255), pos=(450, 8))

    dpg.add_spacer(height=5)

    # ----- ВКЛАДКИ -----
    with dpg.tab_bar():
        
        # Вкладка 1: Aim Assist
        with dpg.tab(label="Aim Assist"):
            dpg.add_spacer(height=10)

            dpg.add_checkbox(label="AimPull", callback=toggle_aimpull)
            with dpg.group(tag="aimpull_settings_group", show=False):
                dpg.add_spacer(height=5)
                with dpg.child_window(height=125, border=True):
                    dpg.add_text("AimPull Settings", color=SOFT_PURPLE)
                    dpg.add_slider_float(
                        label="Smooth", 
                        default_value=aimpull_instance.smooth,
                        min_value=0.1,
                        max_value=10.0,
                        callback=update_smooth,
                        format="%.1f"
                    )
                    dpg.add_slider_int(
                        label="FOV",
                        default_value=aimpull_instance.fov,
                        min_value=10,
                        max_value=200,
                        callback=update_fov
                    )
                    dpg.add_text("Works while holding Left-Click", color=ADDITIONAL_BLACK)

            dpg.add_checkbox(label="Pixel Trigger Bot", callback=toggle_pixel_trigger)
            with dpg.group(tag="trigger_settings_group", show=False):
                dpg.add_spacer(height=5)

                with dpg.child_window(height=140, border=True):
                    dpg.add_text("Trigger Settings", color=SOFT_PURPLE)
                    dpg.add_slider_float(
                        label="Reaction Delay",
                        default_value=pixel_trigger_instance.reaction_delay,
                        min_value=0.005,
                        max_value=0.2,
                        callback=update_pixel_trigger_reaction_delay
                    )
                    dpg.add_slider_int(
                        label="Color Threshold", 
                        default_value=pixel_trigger_instance.threshold, 
                        min_value=1,
                        max_value=100,
                        callback=update_pixel_trigger_threshold
                    )
                    dpg.add_text("Hold L-ALT to scan.\nSmaller threshold = more sensitive trigger.", color=ADDITIONAL_BLACK)

            dpg.add_checkbox(label="AutoPistol", callback=toggle_autopistol)
            with dpg.group(tag="autopistol_settings_group", show=False):
                dpg.add_spacer(height=5)

                with dpg.child_window(height=100, border=True):
                    dpg.add_text("AutoPistol Settings", color=SOFT_PURPLE)
                    dpg.add_slider_float(
                        label="Delay",
                        default_value=autopistol_instance.delay,
                        min_value=0.005,
                        max_value=1.0,
                        callback=update_autopistol_delay,
                        format="%.3f"
                    )
                    dpg.add_text("Hold mouse4 to fire. Lower delay = faster fire rate.", color=ADDITIONAL_BLACK)

            dpg.add_checkbox(label="Mini-Recoil Control", callback=toggle_mrc)
            with dpg.group(tag="mrc_settings_group", show=False):
                dpg.add_spacer(height=5)

                with dpg.child_window(height=125, border=True):
                    dpg.add_text("MRC Settings", color=SOFT_PURPLE)
                    dpg.add_slider_int(
                        label="Strength",
                        default_value=mrc_instance.strength,
                        min_value=1,
                        max_value=6,
                        callback=update_mrc_strength
                    )
                    dpg.add_slider_float(
                        label="Speed",
                        default_value=mrc_instance.speed,
                        min_value=0.005,
                        max_value=0.1,
                        callback=update_mrc_speed,
                        format="%.3f"
                    )
                    dpg.add_text("Hold LMB and script will pull the mouse down.", color=ADDITIONAL_BLACK)

        # Вкладка 2: Anti-Aim
        with dpg.tab(label="Anti-Aim"):
            dpg.add_spacer(height=10)

            dpg.add_checkbox(label="Enable Flick AA", callback=toggle_aa)
            with dpg.group(tag="antiaim_settings_group", show=False):
                dpg.add_spacer(height=5)

                with dpg.child_window(height=125, border=True):
                    dpg.add_text("Flick Anti-Aim Settings", color=SOFT_PURPLE)

                    dpg.add_slider_float(
                        label="Frequency (sec)", 
                        default_value=anti_aim_instance.frequency,
                        min_value=0.02,
                        max_value=2.0,
                        callback=update_aa_frequency,
                        format="%.2f"
                    )

                    dpg.add_slider_int(
                        label="Angle Strength", 
                        default_value=anti_aim_instance.strength,
                        min_value=500,
                        max_value=10000,
                        callback=update_aa_strength
                    )
                    dpg.add_text("Press F in-game to toggle ON/OFF.", color=ADDITIONAL_BLACK)

        # Вкладка 3: Movement
        with dpg.tab(label="Movement"):
            dpg.add_spacer(height=10)

            dpg.add_checkbox(label="Bhop", callback=toggle_bhop)
            with dpg.group(tag="bhop_settings_group", show=False):
                dpg.add_spacer(height=5)

                with dpg.child_window(height=125, border=True):
                    dpg.add_text("Bhop Settings", color=SOFT_PURPLE)
                    dpg.add_checkbox(label="Randomize Jump Offset", callback=toggle_random_offset)
                    dpg.add_slider_float(
                        label="Jump Delay (sec)",
                        default_value=bhop_instance.delay,
                        min_value=0.005,
                        max_value=0.1,
                        callback=update_bhop_delay,
                        format="%.3f"
                    )
                    dpg.add_text("Lower delay = Faster spam. Hold SPACE to bhop.", color=ADDITIONAL_BLACK)

            dpg.add_checkbox(label="Snap Tap", callback=toggle_snap_tap)

        # Вкладка 4: Misc
        with dpg.tab(label="Misc"):
            dpg.add_spacer(height=10)
            dpg.add_checkbox(label="Secured Mode", enabled=False)
            dpg.add_checkbox(label="Anti-AFK", callback=toggle_antiafk)
            dpg.add_checkbox(label="FastZoom", callback=toggle_fastzoom)
            dpg.add_checkbox(label="Zoom to Mouse", enabled=False)
            # configs system
            # theme system

        # Вкладка 5: Keybinds
        with dpg.tab(label="Keybinds"):
            dpg.add_spacer(height=10)
            dpg.add_text("Panic Key: PAUSE (toggle)")
            dpg.add_spacer(height=20)
            dpg.add_text("AimPull: mouse1 (click/hold)")
            dpg.add_text("Pixel Trigger Bot: alt (hold)")
            dpg.add_text("AutoPistol: mouse4 (hold)")
            dpg.add_text("Mini-Recoil Control: mouse1 (hold)")
            dpg.add_spacer(height=10)
            dpg.add_text("Toggle Anti-Aim: F (toggle)")
            dpg.add_spacer(height=10)
            dpg.add_text("Bhop: space (hold)")
            dpg.add_text("Snap Tap: A/D (hold)")
            dpg.add_spacer(height=10)
            dpg.add_text("FastZoom: mouse3 (click/hold)")


# -------------------------- ТЕМА И СТИЛИ --------------------------
with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        # ----- ОКНО -----
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 6)  # Закругление углов окна
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)   # Закругление чекбоксов и полей
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (20, 20, 20, 255))  # Фон окна

        # ----- ЧЕКБОКСЫ -----
        # Цвет галочки (когда включено)
        dpg.add_theme_color(dpg.mvThemeCol_CheckMark, DEEP_PURPLE)
        # Фон чекбокса
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (60, 60, 60, 255))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (80, 80, 80, 255))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (90, 90, 90, 255))

        # ----- ВКЛАДКИ -----
        # Активная вкладка (на которой мы сейчас) - Зеленая, но потемнее
        dpg.add_theme_color(dpg.mvThemeCol_TabActive, DEEP_PURPLE)
        # Обычная вкладка (неактивная)
        dpg.add_theme_color(dpg.mvThemeCol_Tab, (54, 0, 102, 255))
        # При наведении на вкладку
        dpg.add_theme_color(dpg.mvThemeCol_TabHovered, ACTIVE_PURPLE)

        # ----- СЛАЙДЕРЫ -----
        dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, DEEP_PURPLE)
        dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, ACTIVE_PURPLE)


# -------------------------- ЗАПУСК --------------------------
if __name__ == "__main__":
    dpg.bind_theme(global_theme)
    dpg.set_global_font_scale(1.4)  # Увеличение всего UI в 1.4 раза
    dpg.create_viewport(title='ghosthand', width=600, height=420, resizable=False, decorated=True)
    dpg.setup_dearpygui()

    # ----- Запуск скриптов -----
    bhop_instance.start()
    mrc_instance.start()
    autopistol_instance.start()
    antiafk_instance.start()
    pixel_trigger_instance.start()
    snap_tap_instance.start()
    aimpull_instance.start()
    anti_aim_instance.start()
    fastzoom_instance.start()

    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
