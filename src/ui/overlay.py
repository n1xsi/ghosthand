"""
Оверлей GhostHand.

Управляет двумя визуальными элементами:
  - Watermark    : плавающее окошко с тегом wm_title (тематизируемый заголовок)
  - FOV Circle   : круг на drawlist'е внутри основного окна

Rainbow-режим: плавный HSV-цикл на заголовке ватермарки (~30 fps).
При выключении rainbow восстанавливается цвет accent из текущей темы.
"""
import colorsys
import threading
import time

import dearpygui.dearpygui as dpg

from scripts.aimpull import aimpull_instance
from scripts.watermark import watermark_instance
from src.config import VERSION, DEEP_PURPLE

# ── Теги ──────────────────────────────────────────────────────────
_WM_WINDOW = "##wm_window"
_WM_TITLE = "wm_title"  # заголовок ватермарки (тематизируется)
_WM_VERSION = "wm_version"
_FOV_DRAW = "##fov_drawlist"


class OverlayCore:
    def __init__(self):
        self.running = False
        self._hue = 0.0
        self._rainbow_was_on = False  # Флаг для сброса цвета при отключении

    def start(self) -> None:
        self.running = True
        threading.Thread(target=self._init_then_loop, daemon=True).start()

    # ── Инициализация ─────────────────────────────────────────────
    def _init_then_loop(self) -> None:
        time.sleep(0.4)  # Время для DPG, чтобы поднять viewport
        self._build_watermark()
        self._loop()

    def _build_watermark(self) -> None:
        """Создаёт плавающее окошко ватермарки."""
        with dpg.window(
            tag=_WM_WINDOW,
            no_title_bar=True,
            no_move=False,
            no_resize=True,
            no_close=True,
            no_background=False,
            no_scrollbar=True,
            no_scroll_with_mouse=True,
            pos=(10, 10),
            width=145,
            height=38,
            show=False,
        ):
            dpg.add_text("GHOSTHAND", tag=_WM_TITLE, color=DEEP_PURPLE)
            dpg.add_text(VERSION, tag=_WM_VERSION, color=(120, 120, 120, 200))

    # ── Основной цикл ─────────────────────────────────────────────
    def _loop(self) -> None:
        while self.running:
            try:
                self._update_watermark()
                self._update_fov()
            except Exception:
                pass
            time.sleep(0.033)  # ~30 fps

    def _update_watermark(self) -> None:
        enabled = watermark_instance.enabled
        dpg.configure_item(_WM_WINDOW, show=enabled)

        if not enabled:
            return

        if watermark_instance.rainbow:
            # Плавный HSV-цикл по оттенку
            self._hue = (self._hue + 0.003) % 1.0
            r, g, b = colorsys.hsv_to_rgb(self._hue, 1.0, 1.0)
            dpg.configure_item(_WM_TITLE, color=(int(r * 255), int(g * 255), int(b * 255), 255))
            self._rainbow_was_on = True

        elif self._rainbow_was_on:
            # Rainbow только что выключили - восстанавливаем цвет из текущей темы
            from src.ui import theme as _theme
            colors = _theme.get_current_colors()
            accent = colors["accent"] if colors else DEEP_PURPLE
            dpg.configure_item(_WM_TITLE, color=accent)
            self._rainbow_was_on = False

    def _update_fov(self) -> None:
        """Рисует индикатор FOV на drawlist'е внутри основного окна."""
        if not dpg.does_item_exist(_FOV_DRAW):
            return

        dpg.delete_item(_FOV_DRAW, children_only=True)

        if not aimpull_instance.show_fov:
            return

        # Центр экрана в координатах drawlist'а
        try:
            w = dpg.get_viewport_width()
            h = dpg.get_viewport_height()
        except Exception:
            return

        cx, cy = w // 2, h // 2
        r = aimpull_instance.fov

        try:
            color_hex = aimpull_instance.fov_color.lstrip("#")
            cr = int(color_hex[0:2], 16)
            cg = int(color_hex[2:4], 16)
            cb = int(color_hex[4:6], 16)
        except Exception:
            cr, cg, cb = 255, 255, 255

        dpg.draw_circle(
            center=(cx, cy),
            radius=r,
            color=(cr, cg, cb, 180),
            thickness=1.5,
            parent=_FOV_DRAW,
        )


overlay_instance = OverlayCore()
