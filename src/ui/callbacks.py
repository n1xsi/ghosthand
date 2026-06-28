"""
UI Callbacks для GhostHand.

Вместо 30 однотипных функций используются фабрики:
  - _make_toggle(instance, group_tag, label) → callback для чекбоксов вкл/выкл
  - _make_setter(instance, attr, fmt)        → callback для слайдеров/значений
"""
from __future__ import annotations

import dearpygui.dearpygui as dpg

from scripts.aimpull import aimpull_instance
from scripts.anti_aim import anti_aim_instance
from scripts.antiafk import antiafk_instance
from scripts.autopistol import autopistol_instance
from scripts.bunnyhop import bhop_instance
from scripts.fastzoom import fastzoom_instance
from scripts.mrc import mrc_instance
from scripts.pixel_triggerbot import pixel_trigger_instance
from scripts.snaptap import snap_tap_instance
from scripts.turn180 import turn180_instance
from scripts.watermark import watermark_instance

from src.config import (
    THEME_PRESETS,
    BASE_VIEWPORT_WIDTH,
    BASE_VIEWPORT_HEIGHT,
    BASE_STATUS_TEXT_POS,
    STATUS_RIGHT_MARGIN,
    UI_SCALE,
)

# ── Текущий масштаб UI (изменяется через update_ui_scale) ─────────
_current_ui_scale: float = UI_SCALE


# ── Фабрики ───────────────────────────────────────────────────────
def _make_toggle(instance, group_tag: str | None = None, label: str = ""):
    """Фабрика callback'а для чекбокса включения/выключения скрипта."""
    name = label or type(instance).__name__

    def _cb(sender, app_data):
        instance.enabled = app_data
        if group_tag:
            dpg.configure_item(group_tag, show=app_data)
        print(f"[debug-UI] {name} {'ON' if app_data else 'OFF'}")

    return _cb


def _make_setter(instance, attr: str, fmt: str = ""):
    """Фабрика callback'а для слайдера/значения — пишет атрибут экземпляра."""
    def _cb(sender, app_data):
        setattr(instance, attr, app_data)
        value_str = f"{app_data:{fmt}}" if fmt else str(app_data)
        print(f"[debug-UI] {attr} = {value_str}")

    return _cb


# ── AimPull ───────────────────────────────────────────────────────
toggle_aimpull = _make_toggle(aimpull_instance, "aimpull_settings_group", "AimPull")
update_smooth = _make_setter(aimpull_instance, "smooth", ".1f")
update_fov = _make_setter(aimpull_instance, "fov")


def toggle_show_fov(sender, app_data):
    aimpull_instance.show_fov = app_data


def update_fov_color(sender, app_data):
    # DPG возвращает float 0.0–1.0, конвертируем в 0–255
    r, g, b = (int(x * 255) if x <= 1.0 else int(x) for x in app_data[:3])
    aimpull_instance.fov_color = f"#{r:02X}{g:02X}{b:02X}"
    print(f"[debug-UI] FOV Color → #{r:02X}{g:02X}{b:02X}")


# ── Pixel Trigger ─────────────────────────────────────────────────
toggle_pixel_trigger = _make_toggle(pixel_trigger_instance, "trigger_settings_group", "Trigger")
update_pixel_trigger_reaction_delay = _make_setter(pixel_trigger_instance, "reaction_delay", ".4f")
update_pixel_trigger_threshold = _make_setter(pixel_trigger_instance, "threshold")

# ── AutoPistol ────────────────────────────────────────────────────
toggle_autopistol = _make_toggle(autopistol_instance, "autopistol_settings_group", "AutoPistol")
update_autopistol_delay = _make_setter(autopistol_instance, "delay", ".4f")

# ── Mini-Recoil Control ───────────────────────────────────────────
toggle_mrc = _make_toggle(mrc_instance, "mrc_settings_group", "MRC")
update_mrc_strength = _make_setter(mrc_instance, "strength", ".4f")
update_mrc_speed = _make_setter(mrc_instance, "speed",    ".4f")

# ── Anti-Aim ──────────────────────────────────────────────────────
toggle_aa = _make_toggle(anti_aim_instance, "antiaim_settings_group", "Anti-Aim")
update_aa_frequency = _make_setter(anti_aim_instance, "frequency")
update_aa_strength = _make_setter(anti_aim_instance, "strength")

# ── Bhop ──────────────────────────────────────────────────────────
toggle_bhop = _make_toggle(bhop_instance, "bhop_settings_group", "Bhop")
update_bhop_delay = _make_setter(bhop_instance, "delay", ".4f")


def toggle_random_offset(sender, app_data):
    bhop_instance.random_offset = app_data
    print(f"[debug-UI] Bhop random offset {'ON' if app_data else 'OFF'}")


# ── Snap Tap ──────────────────────────────────────────────────────
toggle_snap_tap = _make_toggle(snap_tap_instance, label="SnapTap")

# ── Anti-AFK ──────────────────────────────────────────────────────
toggle_antiafk = _make_toggle(antiafk_instance, label="Anti-AFK")

# ── FastZoom ──────────────────────────────────────────────────────
toggle_fastzoom = _make_toggle(fastzoom_instance, "fastzoom_settings_group", "FastZoom")
toggle_fastzoom_qq_switch = _make_setter(fastzoom_instance, "qq_switch")

# ── Turn180 ───────────────────────────────────────────────────────
toggle_turn180 = _make_toggle(turn180_instance, "turn180_settings_group", "Turn180")
update_turn180_pixels = _make_setter(turn180_instance, "pixels")

# ── Watermark ─────────────────────────────────────────────────────
toggle_watermark = _make_toggle(watermark_instance, "watermark_settings_group", "Watermark")


def toggle_rainbow_watermark(sender, app_data):
    watermark_instance.rainbow = app_data
    print(f"[debug-UI] Rainbow Watermark {'ON' if app_data else 'OFF'}")


def update_watermark_position(sender, app_data):
    watermark_instance.position = app_data
    print(f"[debug-UI] Watermark position → {app_data}")


def toggle_wm_cpu(sender, app_data):
    watermark_instance.show_cpu = app_data
    _update_monitor_label()
 
 
def toggle_wm_gpu(sender, app_data):
    watermark_instance.show_gpu = app_data
    _update_monitor_label()
 
 
def toggle_wm_ping(sender, app_data):
    watermark_instance.show_ping = app_data
    _update_monitor_label()


def _update_monitor_label():
    """Обновляет заголовок collapsing_header по текущему выбору метрик."""
    parts = []
    if watermark_instance.show_cpu:  parts.append("CPU")
    if watermark_instance.show_gpu:  parts.append("GPU")
    if watermark_instance.show_ping: parts.append("Ping")
    label = "Monitor: " + (", ".join(parts) if parts else "None")
    try:
        if dpg.does_item_exist("wm_monitor_header"):
            dpg.configure_item("wm_monitor_header", label=label)
    except Exception:
        pass


# ── UI Scale ──────────────────────────────────────────────────────
def _scale(variable: int, scale: float) -> int:
    """Пересчёт размера от базового масштаба 1.4 к новому."""
    return int(variable / 1.4 * scale)


def update_ui_scale(sender, app_data):
    global _current_ui_scale

    scale = float(app_data.replace("%", "")) / 100
    if scale == _current_ui_scale:
        return

    _current_ui_scale = scale
    watermark_instance.scale = scale  # Overlay подхватит на следующем тике
    dpg.set_global_font_scale(scale)

    new_w = _scale(BASE_VIEWPORT_WIDTH, scale)
    new_h = _scale(BASE_VIEWPORT_HEIGHT, scale)
    dpg.set_viewport_width(new_w)
    dpg.set_viewport_height(new_h)

    new_x = new_w - _scale(STATUS_RIGHT_MARGIN, scale)
    dpg.configure_item("status_text", pos=(new_x, BASE_STATUS_TEXT_POS[1]))

    print(f"[debug-UI] UI Scale → {app_data} ({new_w}x{new_h})")


# ── Темы ──────────────────────────────────────────────────────────
from src.ui import theme as _theme_module  # Импорт после определений во избежание circular


def update_theme_preset(sender, app_data):
    """Колбэк радио-кнопок выбора темы."""
    if app_data == "Custom":
        dpg.configure_item("custom_theme_group", show=True)
        return

    dpg.configure_item("custom_theme_group", show=False)

    # Синхронизрование custom-пикеров с выбранным пресетом
    if app_data in THEME_PRESETS:
        c = THEME_PRESETS[app_data]
        dpg.set_value("ct_accent",       list(c["accent"]))
        dpg.set_value("ct_accent_hover", list(c["accent_hover"]))
        dpg.set_value("ct_tab",          list(c["tab"]))
        dpg.set_value("ct_window_bg",    list(c["window_bg"]))
        dpg.set_value("ct_frame_bg",     list(c["frame_bg"]))
        dpg.set_value("ct_text_accent",  list(c["text_accent"]))

    _theme_module.apply_preset(app_data)


def apply_custom_theme(sender, app_data):
    """Колбэк кнопки «Apply Custom Theme»."""
    def _read(tag: str) -> tuple[int, int, int, int]:
        val = dpg.get_value(tag)
        def _norm(x): return int(x * 255) if x <= 1.0 else int(x)
        r, g, b = _norm(val[0]), _norm(val[1]), _norm(val[2])
        a = _norm(val[3]) if len(val) > 3 else 255
        return (r, g, b, a)

    colors = {
        "accent":       _read("ct_accent"),
        "accent_hover": _read("ct_accent_hover"),
        "tab":          _read("ct_tab"),
        "window_bg":    _read("ct_window_bg"),
        "frame_bg":     _read("ct_frame_bg"),
        "text_accent":  _read("ct_text_accent"),
    }
    _theme_module.apply_colors(colors)
    print("[debug-UI] Custom theme applied")


def reset_theme(sender, app_data):
    """Сброс на дефолтную тему GhostHand — кнопка «Reset» в custom-панели."""
    _theme_module.apply_preset("GhostHand")

    # Сбрасываем радио-кнопку и скрываем custom-панель
    dpg.set_value("theme_radio", "GhostHand")
    dpg.configure_item("custom_theme_group", show=False)

    # Синхронизируем пикеры с GhostHand-пресетом
    c = THEME_PRESETS["GhostHand"]
    dpg.set_value("ct_accent", list(c["accent"]))
    dpg.set_value("ct_accent_hover", list(c["accent_hover"]))
    dpg.set_value("ct_tab", list(c["tab"]))
    dpg.set_value("ct_window_bg", list(c["window_bg"]))
    dpg.set_value("ct_frame_bg", list(c["frame_bg"]))
    dpg.set_value("ct_text_accent", list(c["text_accent"]))

    print("[debug-UI] Theme reset → GhostHand")
