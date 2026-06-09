"""
GUI-строитель GhostHand.

build_gui() вызывается один раз из main.py после dpg.create_context().
Каждая вкладка оформлена отдельной приватной функцией.
"""
import dearpygui.dearpygui as dpg

from scripts.aimpull import aimpull_instance
from scripts.anti_aim import anti_aim_instance
from scripts.autopistol import autopistol_instance
from scripts.bunnyhop import bhop_instance
from scripts.fastzoom import fastzoom_instance
from scripts.mrc import mrc_instance
from scripts.pixel_triggerbot import pixel_trigger_instance
from scripts.turn180 import turn180_instance

from src.config import (
    DEEP_PURPLE,
    SOFT_PURPLE,
    ACTIVE_PURPLE,
    ADDITIONAL_BLACK,
    BASE_VIEWPORT_WIDTH,
    BASE_VIEWPORT_HEIGHT,
    BASE_STATUS_TEXT_POS,
    VERSION,
)
from src.ui.callbacks import (
    toggle_aimpull, update_smooth, update_fov,
    toggle_show_fov, update_fov_color,
    toggle_pixel_trigger, update_pixel_trigger_reaction_delay, update_pixel_trigger_threshold,
    toggle_autopistol, update_autopistol_delay,
    toggle_mrc, update_mrc_strength, update_mrc_speed,
    toggle_aa, update_aa_frequency, update_aa_strength,
    toggle_bhop, update_bhop_delay, toggle_random_offset,
    toggle_snap_tap,
    toggle_antiafk,
    toggle_fastzoom, toggle_fastzoom_qq_switch,
    toggle_turn180, update_turn180_pixels,
    toggle_watermark, update_ui_scale,
    update_theme_preset, apply_custom_theme,
)


# ── Вкладки ───────────────────────────────────────────────────────

def _tab_aim():
    with dpg.tab(label="Aim Assist"):
        dpg.add_spacer(height=10)

        dpg.add_checkbox(label="AimPull", callback=toggle_aimpull)
        with dpg.group(tag="aimpull_settings_group", show=False):
            dpg.add_spacer(height=5)
            with dpg.child_window(height=205, border=True):
                dpg.add_text("AimPull Settings", color=SOFT_PURPLE, tag="header_aimpull")
                dpg.add_slider_float(
                    label="Smooth",
                    default_value=aimpull_instance.smooth,
                    min_value=0.1, max_value=10.0,
                    callback=update_smooth, format="%.1f",
                )
                dpg.add_slider_int(
                    label="FOV",
                    default_value=aimpull_instance.fov,
                    min_value=10, max_value=600,
                    callback=update_fov,
                )
                dpg.add_spacer(height=5)
                dpg.add_separator()
                dpg.add_spacer(height=5)
                dpg.add_checkbox(label="Draw FOV Circle", callback=toggle_show_fov)
                dpg.add_color_edit(
                    label="FOV Color",
                    default_value=(255, 255, 255, 255),
                    no_alpha=True,
                    callback=update_fov_color,
                )
                dpg.add_text("Pulls to the red color while holding Left-Click.", color=ADDITIONAL_BLACK)

        dpg.add_checkbox(label="Pixel Trigger Bot", callback=toggle_pixel_trigger)
        with dpg.group(tag="trigger_settings_group", show=False):
            dpg.add_spacer(height=5)
            with dpg.child_window(height=140, border=True):
                dpg.add_text("Trigger Settings", color=SOFT_PURPLE, tag="header_trigger")
                dpg.add_slider_float(
                    label="Reaction Delay",
                    default_value=pixel_trigger_instance.reaction_delay,
                    min_value=0.005, max_value=0.2,
                    callback=update_pixel_trigger_reaction_delay,
                )
                dpg.add_slider_int(
                    label="Color Threshold",
                    default_value=pixel_trigger_instance.threshold,
                    min_value=1, max_value=100,
                    callback=update_pixel_trigger_threshold,
                )
                dpg.add_text(
                    "Hold L-ALT to pixel scan and lock the mouse.\n"
                    "Smaller threshold = more sensitive trigger.",
                    color=ADDITIONAL_BLACK,
                )

        dpg.add_checkbox(label="AutoPistol", callback=toggle_autopistol)
        with dpg.group(tag="autopistol_settings_group", show=False):
            dpg.add_spacer(height=5)
            with dpg.child_window(height=100, border=True):
                dpg.add_text("AutoPistol Settings", color=SOFT_PURPLE, tag="header_autopistol")
                dpg.add_slider_float(
                    label="Delay",
                    default_value=autopistol_instance.delay,
                    min_value=0.005, max_value=1.0,
                    callback=update_autopistol_delay, format="%.3f",
                )
                dpg.add_text("Hold mouse4 to fire. Lower delay = faster fire rate.", color=ADDITIONAL_BLACK)

        dpg.add_checkbox(label="Mini-Recoil Control", callback=toggle_mrc)
        with dpg.group(tag="mrc_settings_group", show=False):
            dpg.add_spacer(height=5)
            with dpg.child_window(height=125, border=True):
                dpg.add_text("MRC Settings", color=SOFT_PURPLE, tag="header_mrc")
                dpg.add_slider_int(
                    label="Strength",
                    default_value=mrc_instance.strength,
                    min_value=1, max_value=6,
                    callback=update_mrc_strength,
                )
                dpg.add_slider_float(
                    label="Speed",
                    default_value=mrc_instance.speed,
                    min_value=0.005, max_value=0.1,
                    callback=update_mrc_speed, format="%.3f",
                )
                dpg.add_text("Hold LMB and script will pull the mouse down.", color=ADDITIONAL_BLACK)


def _tab_antiaim():
    with dpg.tab(label="Anti-Aim"):
        dpg.add_spacer(height=10)

        dpg.add_checkbox(label="Enable Flick AA", callback=toggle_aa)
        with dpg.group(tag="antiaim_settings_group", show=False):
            dpg.add_spacer(height=5)
            with dpg.child_window(height=125, border=True):
                dpg.add_text("Flick Anti-Aim Settings", color=SOFT_PURPLE, tag="header_antiaim")
                dpg.add_slider_float(
                    label="Frequency (sec)",
                    default_value=anti_aim_instance.frequency,
                    min_value=0.02, max_value=2.0,
                    callback=update_aa_frequency, format="%.2f",
                )
                dpg.add_slider_int(
                    label="Angle Strength",
                    default_value=anti_aim_instance.strength,
                    min_value=500, max_value=10000,
                    callback=update_aa_strength,
                )
                dpg.add_text("Press F in-game to toggle ON/OFF.", color=ADDITIONAL_BLACK)


def _tab_movement():
    with dpg.tab(label="Movement"):
        dpg.add_spacer(height=10)

        dpg.add_checkbox(label="Bhop", callback=toggle_bhop)
        with dpg.group(tag="bhop_settings_group", show=False):
            dpg.add_spacer(height=5)
            with dpg.child_window(height=125, border=True):
                dpg.add_text("Bhop Settings", color=SOFT_PURPLE, tag="header_bhop")
                dpg.add_checkbox(label="Randomize Jump Offset", callback=toggle_random_offset)
                dpg.add_slider_float(
                    label="Jump Delay (sec)",
                    default_value=bhop_instance.delay,
                    min_value=0.005, max_value=0.3,
                    callback=update_bhop_delay, format="%.3f",
                )
                dpg.add_text("Lower delay = Faster spam. Hold SPACE to bhop.", color=ADDITIONAL_BLACK)

        dpg.add_checkbox(label="Snap Tap", callback=toggle_snap_tap)


def _tab_visuals():
    with dpg.tab(label="Visuals"):
        dpg.add_spacer(height=10)
        dpg.add_checkbox(label="Crosshair", enabled=False)
        dpg.add_checkbox(label="Watermark", callback=toggle_watermark)

        dpg.add_spacer(height=8)
        dpg.add_separator()
        dpg.add_spacer(height=6)

        dpg.add_text("Theme", color=SOFT_PURPLE)
        dpg.add_radio_button(
            tag="theme_radio",
            items=["GhostHand", "Black & White", "Razer", "Custom"],
            default_value="GhostHand",
            horizontal=True,
            callback=update_theme_preset,
        )

        # ── Custom-панель (скрыта по умолчанию) ──────────────────
        with dpg.group(tag="custom_theme_group", show=False):
            dpg.add_spacer(height=5)
            with dpg.child_window(height=202, border=True):
                dpg.add_text("Custom Theme", color=SOFT_PURPLE, tag="header_custom_theme")
                dpg.add_color_edit(
                    label="Accent", tag="ct_accent",
                    default_value=list(DEEP_PURPLE), no_alpha=True,
                )
                dpg.add_color_edit(
                    label="Accent Hover", tag="ct_accent_hover",
                    default_value=list(ACTIVE_PURPLE), no_alpha=True,
                )
                dpg.add_color_edit(
                    label="Tab BG", tag="ct_tab",
                    default_value=[54, 0, 102, 255], no_alpha=True,
                )
                dpg.add_color_edit(
                    label="Window BG", tag="ct_window_bg",
                    default_value=[20, 20, 20, 255], no_alpha=True,
                )
                dpg.add_color_edit(
                    label="Frame BG", tag="ct_frame_bg",
                    default_value=[60, 60, 60, 255], no_alpha=True,
                )
                dpg.add_color_edit(
                    label="Header Text", tag="ct_text_accent",
                    default_value=list(SOFT_PURPLE), no_alpha=True,
                )
                dpg.add_spacer(height=4)
                dpg.add_button(label="Apply Custom Theme", callback=apply_custom_theme, width=-1)

        dpg.add_spacer(height=8)
        dpg.add_separator()
        dpg.add_spacer(height=6)

        dpg.add_combo(
            label="UI Scale",
            items=["100%", "125%", "140%", "150%", "175%", "200%"],
            default_value="140%",
            callback=update_ui_scale,
        )


def _tab_misc():
    with dpg.tab(label="Misc"):
        dpg.add_spacer(height=10)
        dpg.add_checkbox(label="Secured Mode", enabled=False)
        dpg.add_checkbox(label="Anti-AFK", callback=toggle_antiafk)

        dpg.add_checkbox(label="FastZoom", callback=toggle_fastzoom)
        with dpg.group(tag="fastzoom_settings_group", show=False):
            dpg.add_spacer(height=5)
            with dpg.child_window(height=115, border=True):
                dpg.add_text("FastZoom Settings", color=SOFT_PURPLE, tag="header_fastzoom")
                dpg.add_checkbox(
                    label="Q-Q switch",
                    callback=toggle_fastzoom_qq_switch,
                    default_value=fastzoom_instance.qq_switch,
                )
                dpg.add_text(
                    "Click mouse3 to zoom + shot\n(+ weapon fastswitch if enabled).",
                    color=ADDITIONAL_BLACK,
                )

        dpg.add_checkbox(label="Zoom to Mouse", enabled=False)

        dpg.add_checkbox(label="180°-turn", callback=toggle_turn180)
        with dpg.group(tag="turn180_settings_group", show=False):
            dpg.add_spacer(height=5)
            with dpg.child_window(height=125, border=True):
                dpg.add_text("Turn Settings", color=SOFT_PURPLE, tag="header_turn180")
                dpg.add_slider_int(
                    label="Distance (Pixels)",
                    default_value=turn180_instance.pixels,
                    min_value=500, max_value=10000,
                    callback=update_turn180_pixels,
                )
                dpg.add_text("Press T to turn. Turn off your mouse acceleration.", color=ADDITIONAL_BLACK)
                dpg.add_text("Adjust the slider until you do exactly a 180 turn.", color=ADDITIONAL_BLACK)


def _tab_keybinds():
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


# ── Точка входа ───────────────────────────────────────────────────

def build_gui() -> None:
    """Строит весь интерфейс. Вызывать после dpg.create_context()."""
    with dpg.window(
        tag="Primary Window",
        width=BASE_VIEWPORT_WIDTH,
        height=BASE_VIEWPORT_HEIGHT,
        no_resize=True,
        no_move=True,
        no_collapse=True,
        no_title_bar=True,
    ):
        # Заголовок
        with dpg.group(horizontal=True):
            dpg.add_text("GHOSTHAND", color=DEEP_PURPLE, tag="title_text")
            dpg.add_text(VERSION, color=ADDITIONAL_BLACK)
            dpg.add_text("SYSTEM ACTIVE", tag="status_text", color=(50, 255, 50, 255), pos=BASE_STATUS_TEXT_POS)

        dpg.add_spacer(height=5)

        with dpg.tab_bar():
            _tab_aim()
            _tab_antiaim()
            _tab_movement()
            _tab_visuals()
            _tab_misc()
            _tab_keybinds()
