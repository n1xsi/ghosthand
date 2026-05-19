"""
UI Callbacks для GhostHand.

Вместо однотипных функций используются фабрики:
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
toggle_watermark = _make_toggle(watermark_instance, label="Watermark")

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
    dpg.set_global_font_scale(scale)

    new_w = _scale(BASE_VIEWPORT_WIDTH, scale)
    new_h = _scale(BASE_VIEWPORT_HEIGHT, scale)
    dpg.set_viewport_width(new_w)
    dpg.set_viewport_height(new_h)

    new_x = new_w - _scale(STATUS_RIGHT_MARGIN, scale)
    dpg.configure_item("status_text", pos=(new_x, BASE_STATUS_TEXT_POS[1]))

    print(f"[debug-UI] UI Scale → {app_data} ({new_w}x{new_h})")
