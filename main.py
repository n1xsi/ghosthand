from scripts.pixel_triggerbot import pixel_trigger_instance
from scripts.autopistol import autopistol_instance
from scripts.watermark import watermark_instance
from scripts.anti_aim import anti_aim_instance
from scripts.fastzoom import fastzoom_instance
from scripts.snaptap import snap_tap_instance
from scripts.antiafk import antiafk_instance
from scripts.aimpull import aimpull_instance
from scripts.turn180 import turn180_instance
from scripts.bunnyhop import bhop_instance
from scripts.mrc import mrc_instance
import scripts.panic

from src.ui.overlay import overlay_instance

import dearpygui.dearpygui as dpg


# Глобальные переменные
DEEP_PURPLE = (139, 0, 255, 255)
SOFT_PURPLE = (163, 102, 255, 255)
ACTIVE_PURPLE = (184, 102, 255, 255)
ADDITIONAL_BLACK = (150, 150, 150, 200)

BASE_VIEWPORT_WIDTH = 600
BASE_VIEWPORT_HEIGHT = 420

BASE_STATUS_TEXT_POS = (440, 8)
STATUS_RIGHT_MARGIN = 160  # px при дефолтном 140%

UI_SCALE = 1.4
VERSION = "v0.9.1 Dev Build"

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
    dpg.configure_item("fastzoom_settings_group", show=app_data)
    print(f"[debug-UI] Fast-Zoom is {"ON" if app_data else "OFF"}")


def toggle_fastzoom_qq_switch(sender, app_data):
    fastzoom_instance.qq_switch = app_data
    print(f"[debug-UI] Fast-Zoom Q-Q switch is {"ON" if app_data else "OFF"}")

# ----- turn180 -----
def toggle_turn180(sender, app_data):
    turn180_instance.enabled = app_data
    dpg.configure_item("turn180_settings_group", show=app_data)
    print(f"[debug-UI] turn180 is {"ON" if app_data else "OFF"}")


def update_turn180_pixels(sender, app_data):
    turn180_instance.pixels = app_data

# ----- ui scale -----
to_new_size = lambda variable, scale: int(variable / 1.4 * scale)  # Деление на базовый мастаб (1.4)


def update_ui_scale(sender, app_data):
    global UI_SCALE

    scale_float = float(app_data.replace("%", "")) / 100

    if scale_float == UI_SCALE:
        return

    UI_SCALE = scale_float
    dpg.set_global_font_scale(scale_float)

    new_width = to_new_size(BASE_VIEWPORT_WIDTH, scale_float)
    new_height = to_new_size(BASE_VIEWPORT_HEIGHT, scale_float)

    dpg.set_viewport_width(new_width)
    dpg.set_viewport_height(new_height)

    new_status_text_pos = new_width - to_new_size(STATUS_RIGHT_MARGIN, scale_float)
    dpg.configure_item("status_text", pos=(new_status_text_pos, BASE_STATUS_TEXT_POS[1]))

    print(f"[debug-UI] UI Scale set to {app_data} ({new_width}x{new_height})")

# -------------------------- OVERLAY --------------------------
def toggle_show_fov(sender, app_data):
    aimpull_instance.show_fov = app_data


def update_fov_color(sender, app_data):
    # DearPyGui возвращает сырые float от 0.0 до 1.0 =>
    # => умножаем их на 255, чтобы получить стандартный RGB (0-255)
    r, g, b = map(lambda x: int(x * 255) if x <= 1.0 else int(x), app_data[:3])

    hex_color = f"#{r:02X}{g:02X}{b:02X}"
    aimpull_instance.fov_color = hex_color
    print(f"[debug-UI] FOV Color set to: {hex_color}")


def toggle_watermark(sender, app_data):
    watermark_instance.enabled = app_data
    print(f"[debug-UI] Watermark is {'ON' if app_data else 'OFF'}")


# -------------------------- GUI SETUP --------------------------
dpg.create_context()  # Инициализация DearPyGui

with dpg.window(tag="Primary Window", width=BASE_VIEWPORT_WIDTH, height=BASE_VIEWPORT_HEIGHT , no_resize=True, no_move=True, no_collapse=True, no_title_bar=True):

    # Заголовок
    with dpg.group(horizontal=True):
        dpg.add_text("GHOSTHAND", color=DEEP_PURPLE)
        dpg.add_text(VERSION, color=ADDITIONAL_BLACK)
        dpg.add_text("SYSTEM ACTIVE", tag="status_text", color=(50, 255, 50, 255), pos=BASE_STATUS_TEXT_POS)

    dpg.add_spacer(height=5)

    # ----- ВКЛАДКИ -----
    with dpg.tab_bar():

        # Вкладка 1: Aim Assist
        with dpg.tab(label="Aim Assist"):
            dpg.add_spacer(height=10)

            dpg.add_checkbox(label="AimPull", callback=toggle_aimpull)
            with dpg.group(tag="aimpull_settings_group", show=False):
                dpg.add_spacer(height=5)
                with dpg.child_window(height=205, border=True):
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
                        max_value=600,
                        callback=update_fov
                    )
                    dpg.add_spacer(height=5)
                    dpg.add_separator()
                    dpg.add_spacer(height=5)
                    dpg.add_checkbox(label="Draw FOV Circle", callback=toggle_show_fov)
                    dpg.add_color_edit(label="FOV Color", default_value=(255, 255, 255, 255), no_alpha=True, callback=update_fov_color)
                    dpg.add_text("Pulls to the red color while holding Left-Click.", color=ADDITIONAL_BLACK)

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
                    dpg.add_text("Hold L-ALT to pixel scan and lock the mouse.\nSmaller threshold = more sensitive trigger.", color=ADDITIONAL_BLACK)

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
                        max_value=0.3,
                        callback=update_bhop_delay,
                        format="%.3f"
                    )
                    dpg.add_text("Lower delay = Faster spam. Hold SPACE to bhop.", color=ADDITIONAL_BLACK)

            dpg.add_checkbox(label="Snap Tap", callback=toggle_snap_tap)

        # Вкладка 4: Visuals
        with dpg.tab(label="Visuals"):
            dpg.add_spacer(height=10)
            dpg.add_checkbox(label="Crosshair", enabled=False)
            dpg.add_checkbox(label="Watermark", callback=toggle_watermark)
            dpg.add_combo(
                label="UI Scale", 
                items=["100%", "125%", "140%", "150%", "175%", "200%"], 
                default_value="140%", 
                callback=update_ui_scale
            )
            dpg.add_combo(label="Theme", items=["Default", "Dark", "Purple"], default_value="Default")

        # Вкладка 5: Misc
        with dpg.tab(label="Misc"):
            dpg.add_spacer(height=10)
            dpg.add_checkbox(label="Secured Mode", enabled=False)
            dpg.add_checkbox(label="Anti-AFK", callback=toggle_antiafk)

            dpg.add_checkbox(label="FastZoom", callback=toggle_fastzoom)
            with dpg.group(tag="fastzoom_settings_group", show=False):
                dpg.add_spacer(height=5)
                with dpg.child_window(height=115, border=True):
                    dpg.add_text("FastZoom Settings", color=SOFT_PURPLE)
                    dpg.add_checkbox(label="Q-Q switch", callback=toggle_fastzoom_qq_switch, default_value=fastzoom_instance.qq_switch)
                    dpg.add_text("Click mouse3 to zoom + shot\n(+ weapon fastswitch if enabled).", color=ADDITIONAL_BLACK)

            dpg.add_checkbox(label="Zoom to Mouse", enabled=False)

            dpg.add_checkbox(label="180°-turn", callback=toggle_turn180)
            with dpg.group(tag="turn180_settings_group", show=False):
                dpg.add_spacer(height=5)
                with dpg.child_window(height=125, border=True):
                    dpg.add_text("Turn Settings", color=SOFT_PURPLE)
                    dpg.add_slider_int(
                        label="Distance (Pixels)",
                        default_value=turn180_instance.pixels,
                        min_value=500,
                        max_value=10000,
                        callback=update_turn180_pixels
                    )
                    dpg.add_text("Press T to turn. Turn off your mouse acceleration.", color=ADDITIONAL_BLACK)
                    dpg.add_text("Adjust the slider until you do exactly a 180 turn.", color=ADDITIONAL_BLACK)

        # Вкладка 6: Keybinds
        with dpg.tab(label="Keybinds"):
            dpg.add_spacer(height=10)
            dpg.add_text("Panic Key: PAUSE (toggle)")
            dpg.add_spacer(height=10)
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
            dpg.add_text("180°-turn: T (click)")


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
    dpg.set_global_font_scale(UI_SCALE)

    # Установка размеров окна и его параметров (неизменяемое, без рамки)
    dpg.create_viewport(title='ghosthand', width=BASE_VIEWPORT_WIDTH, height=BASE_VIEWPORT_HEIGHT, resizable=False, decorated=True)

    # Установка иконки
    try:
        icon_path = "assets/icon.ico"
        dpg.set_viewport_small_icon(icon_path)
        dpg.set_viewport_large_icon(icon_path)
    except Exception as e:
        print(f"[debug-UI] Не удалось загрузить иконку: {e}")


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
    turn180_instance.start()

    overlay_instance.start()

    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
