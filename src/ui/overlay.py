from scripts.watermark import watermark_instance
from scripts.aimpull import aimpull_instance
from scripts.soundesp import soundesp_instance
from src.core.sysmon import sysmon
from src.core import input_sim
from src.config import (
    VERSION,
    DEEP_PURPLE_HEX,
    WM_BG_FILL, WM_BG_OUTLINE, WM_TEXT_COLOR,
    WM_STATUS_ACTIVE, WM_STATUS_PAUSE, WM_WARN_COLOR,
    WM_MARGIN, WM_PAD_X, WM_PAD_Y, WM_HEADER_H,
    WM_FONT_NAME, WM_FONT_BASE, WM_FONT_MIN,
    CPU_WARN_THRESHOLD, GPU_WARN_THRESHOLD, RAM_WARN_THRESHOLD, PING_WARN_THRESHOLD,
    UI_SCALE,
    SE_ARROW_SLOTS, SE_COLOR_FADE, SE_UNSURE_COLOR, SE_MIN_INTENSITY,
)

import colorsys
import math
import tkinter as tk
import tkinter.font as tkfont
import threading
import ctypes
import time

WS_EX_TRANSPARENT = 0x00000020
GWL_EXSTYLE = -20


class MasterOverlay:
    def __init__(self):
        # Состояние оверлея
        self.running = False
        self.root = None
        self.canvas = None

        # Графические объекты
        self.circle_id = None
        self.wm_bg = None
        self.wm_header = None
        self.wm_text_prefix = None   # Надпись "GHOSTHAND"
        self.wm_text_version = None  # Версия билда
        self.wm_text_status = None   # Надпись "GLOBAL PAUSE" или "SYSTEM ACTIVE"
        self.wm_text_suffix = None   # Время в формате "HH:MM:SS"
        self.wm_text_cpu = None
        self.wm_text_gpu = None
        self.wm_text_ram = None
        self.wm_text_ping = None

        # Пул стрелок Sound ESP
        self.se_arrows = []

        # Реальное разрешение экрана
        self.screen_width = 0
        self.screen_height = 0

        # Rainbow
        self._hue = 0.0
        self._last_scale = UI_SCALE
        self._tk_font = None  # tkinter Font object для measure()
        self._text_h = 14  # Высота строки в пикселях (обновляется с масштабом)

    # ── Запуск ────────────────────────────────────────────────────
    def start(self):
        self.running = True
        threading.Thread(target=self._run_tk, daemon=True).start()

    def _run_tk(self):
        try:
            # DPI-fix: 1 пиксель tkinter = 1 физический пиксель монитора
            ctypes.windll.user32.SetProcessDPIAware()

            self.root = tk.Tk()
            self.root.overrideredirect(True)
            self.root.wm_attributes("-topmost", True)
            self.root.wm_attributes("-transparentcolor", "black")
            self.root.config(bg="black")

            # Реальное разрешение через WinAPI (игнорируем масштаб Windows)
            self.screen_width = ctypes.windll.user32.GetSystemMetrics(0)
            self.screen_height = ctypes.windll.user32.GetSystemMetrics(1)
            self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")

            # Click-Through: клики проходят сквозь оверлей к игре
            self.root.update_idletasks()
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_TRANSPARENT)

            self.canvas = tk.Canvas(
                self.root,
                width=self.screen_width, height=self.screen_height,
                bg="black", bd=0, highlightthickness=0, relief="ridge",
            )
            self.canvas.pack(fill="both", expand=True)

            # Создаём Font-объект — для measure() ширина текста без canvas.bbox()
            font_size = self._calc_font_size(watermark_instance.scale)
            self._tk_font = tkfont.Font(
                family=WM_FONT_NAME, size=font_size, weight="bold"
            )
            self._text_h = self._tk_font.metrics("linespace")
            font_tuple = (WM_FONT_NAME, font_size, "bold")

            self.circle_id = self.canvas.create_oval(0, 0, 0, 0, outline=WM_TEXT_COLOR, width=2)
            self.wm_bg = self.canvas.create_rectangle(0, 0, 0, 0, fill=WM_BG_FILL, outline=WM_BG_OUTLINE, width=1)
            self.wm_header = self.canvas.create_rectangle(0, 0, 0, 0, fill=DEEP_PURPLE_HEX, outline="")
            self.wm_text_prefix = self.canvas.create_text(0, 0, text="", fill=WM_TEXT_COLOR, font=font_tuple, anchor="nw")
            self.wm_text_version = self.canvas.create_text(0, 0, text="", fill=WM_TEXT_COLOR, font=font_tuple, anchor="nw")
            self.wm_text_status = self.canvas.create_text(0, 0, text="", fill=WM_TEXT_COLOR, font=font_tuple, anchor="nw")
            self.wm_text_suffix = self.canvas.create_text(0, 0, text="", fill=WM_TEXT_COLOR, font=font_tuple, anchor="nw")
            self.wm_text_cpu = self.canvas.create_text(0, 0, text="", fill=WM_TEXT_COLOR, font=font_tuple, anchor="nw")
            self.wm_text_gpu = self.canvas.create_text(0, 0, text="", fill=WM_TEXT_COLOR, font=font_tuple, anchor="nw")
            self.wm_text_ram = self.canvas.create_text(0, 0, text="", fill=WM_TEXT_COLOR, font=font_tuple, anchor="nw")
            self.wm_text_ping = self.canvas.create_text(0, 0, text="", fill=WM_TEXT_COLOR, font=font_tuple, anchor="nw")

            # Пул треугольников для Sound ESP
            self.se_arrows = [
                self.canvas.create_polygon(0, 0, 0, 0, 0, 0, fill=SE_COLOR_FADE, state="hidden")
                for _ in range(SE_ARROW_SLOTS)
            ]

            print(f"[debug:overlay] Initialized. Resolution: {self.screen_width}x{self.screen_height}")
            self.update_loop()
            self.root.mainloop()

        except Exception as e:
            print(f"[debug:overlay] Failed to start: {e}")

    # ── Вспомогательные методы ────────────────────────────────────
    @staticmethod
    def _calc_font_size(scale: float) -> int:
        return max(WM_FONT_MIN, round(WM_FONT_BASE * scale / 1.4))

    def _w(self, text: str) -> int:
        """Ширина строки в пикселях через Font.measure() — без canvas.bbox()."""
        return self._tk_font.measure(text)

    def _header_color(self) -> str:
        """Rainbow → HSV-цикл. Иначе → accent текущей темы."""
        if watermark_instance.rainbow:
            self._hue = (self._hue + 0.003) % 1.0
            r, g, b = colorsys.hsv_to_rgb(self._hue, 1.0, 1.0)
            return f"#{int(r * 255):02X}{int(g * 255):02X}{int(b * 255):02X}"
        try:
            from src.ui import theme as _theme
            colors = _theme.get_current_colors()
            if colors:
                r, g, b = colors["accent"][:3]
                return f"#{r:02X}{g:02X}{b:02X}"
        except Exception:
            pass
        return DEEP_PURPLE_HEX

    def _calc_position(self, rect_w: int, rect_h: int) -> tuple[int, int]:
        pos = watermark_instance.position
        sw, sh, m = self.screen_width, self.screen_height, WM_MARGIN
        return {
            "Top Left":      (m,                  m),
            "Top Center":    ((sw - rect_w) // 2, m),
            "Top Right":     (sw - rect_w - m,    m),
            "Bottom Left":   (m,                  sh - rect_h - m),
            "Bottom Center": ((sw - rect_w) // 2, sh - rect_h - m),
            "Bottom Right":  (sw - rect_w - m,    sh - rect_h - m),
        }.get(pos, (sw - rect_w - m, m))

    # ── Главный цикл (16 мс ≈ 60 fps) ────────────────────────────
    def update_loop(self):
        if not self.running:
            self.root.destroy()
            return

        try:
            # Смена масштаба шрифта
            cur_scale = watermark_instance.scale
            if cur_scale != self._last_scale:
                self._last_scale = cur_scale
                font_size = self._calc_font_size(cur_scale)
                font_tuple = (WM_FONT_NAME, font_size, "bold")
                self._tk_font.config(size=font_size)
                self._text_h = self._tk_font.metrics("linespace")
                for item in (self.wm_text_prefix, self.wm_text_version, self.wm_text_status, self.wm_text_suffix,
                             self.wm_text_cpu, self.wm_text_gpu, self.wm_text_ram, self.wm_text_ping):
                    self.canvas.itemconfig(item, font=font_tuple)

            # ── FOV Circle ────────────────────────────────────────
            if aimpull_instance.show_fov and aimpull_instance.enabled:
                fov = aimpull_instance.fov
                cx, cy = self.screen_width // 2, self.screen_height // 2
                self.canvas.coords(self.circle_id, cx - fov,
                                   cy - fov, cx + fov, cy + fov)
                self.canvas.itemconfig(self.circle_id, outline=aimpull_instance.fov_color, state="normal")
            else:
                self.canvas.itemconfig(self.circle_id, state="hidden")

            # ── Sound ESP ─────────────────────────────────────────
            if soundesp_instance.enabled:
                self._draw_sound_esp()
            else:
                for item in self.se_arrows:
                    self.canvas.itemconfig(item, state="hidden")

            # ── Watermark ─────────────────────────────────────────
            if watermark_instance.enabled:
                self._draw_watermark()
            else:
                for item in (self.wm_bg, self.wm_header, self.wm_text_prefix,
                             self.wm_text_version, self.wm_text_status, self.wm_text_suffix,
                             self.wm_text_cpu, self.wm_text_gpu, self.wm_text_ram, self.wm_text_ping):
                    self.canvas.itemconfig(item, state="hidden")

        except Exception as e:
            print(f"[debug:overlay] Update loop crashed: {e}")

        self.root.after(16, self.update_loop)

    # ── Отрисовка Sound ESP ───────────────────────────────────────
    @staticmethod
    def _fade_color(peak: str, floor: str, t: float) -> str:
        """Линейная интерполяция между двумя hex-цветами, t: 0 = floor, 1 = peak."""
        t = max(0.0, min(1.0, t))
        pr, pg, pb = int(peak[1:3], 16), int(peak[3:5], 16), int(peak[5:7], 16)
        fr, fg, fb = int(floor[1:3], 16), int(floor[3:5], 16), int(floor[5:7], 16)
        r = round(fr + (pr - fr) * t)
        g = round(fg + (pg - fg) * t)
        b = round(fb + (pb - fb) * t)
        return f"#{r:02X}{g:02X}{b:02X}"

    def _draw_sound_esp(self):
        se = soundesp_instance
        arrows = se.active_arrows()

        cx, cy = self.screen_width // 2, self.screen_height // 2
        radius, size = se.radius, se.size

        for slot, item in enumerate(self.se_arrows):
            if slot >= len(arrows):
                self.canvas.itemconfig(item, state="hidden")
                continue

            angle, intensity, fb_known = arrows[slot]
            if intensity < SE_MIN_INTENSITY:
                self.canvas.itemconfig(item, state="hidden")
                continue

            # 0° = вверх (вперёд), + = по часовой (вправо).
            # Экранный Y растёт вниз, поэтому вершина = -cos.
            rad = math.radians(angle)
            sin_a, cos_a = math.sin(rad), math.cos(rad)

            # Кончик стрелки смотрит наружу от центра
            tip_x = cx + sin_a * (radius + size)
            tip_y = cy - cos_a * (radius + size)

            # Основание - перпендикуляр к направлению
            base_x = cx + sin_a * radius
            base_y = cy - cos_a * radius
            half = size * 0.45
            left_x = base_x - cos_a * half
            left_y = base_y - sin_a * half
            right_x = base_x + cos_a * half
            right_y = base_y + sin_a * half

            # Недостоверная ось перед/зад (стерео + невнятный тембр) => серый
            base_color = se.color if fb_known else SE_UNSURE_COLOR
            color = self._fade_color(base_color, SE_COLOR_FADE, intensity)

            self.canvas.coords(item, tip_x, tip_y, left_x, left_y, right_x, right_y)
            self.canvas.itemconfig(item, fill=color, state="normal")

    # ── Отрисовка ватермарки ──────────────────────────────────────
    def _draw_watermark(self):
        wm = watermark_instance

        # ── Тексты и цвета сегментов ──────────────────────────────
        st_txt = "GLOBAL PAUSE" if input_sim.GLOBAL_PAUSE else "SYSTEM ACTIVE"
        st_color = WM_STATUS_PAUSE if input_sim.GLOBAL_PAUSE else WM_STATUS_ACTIVE

        cpu_str = f" | CPU: {sysmon.cpu_percent:.0f}%"
        gpu_str = f" | GPU: {sysmon.gpu_percent:.0f}%"
        ram_str = f" | RAM: {sysmon.ram_percent:.0f}%"
        ping_str = f" | Ping: {sysmon.ping_ms}ms"

        cpu_color = WM_WARN_COLOR if sysmon.cpu_percent >= CPU_WARN_THRESHOLD else WM_TEXT_COLOR
        gpu_color = WM_WARN_COLOR if sysmon.gpu_percent >= GPU_WARN_THRESHOLD else WM_TEXT_COLOR
        ram_color = WM_WARN_COLOR if sysmon.ram_percent >= RAM_WARN_THRESHOLD else WM_TEXT_COLOR
        ping_color = WM_WARN_COLOR if sysmon.ping_ms >= PING_WARN_THRESHOLD else WM_TEXT_COLOR

        segments = [
            (self.wm_text_prefix, "GHOSTHAND" if wm.show_version else "GHOSTHAND | ", WM_TEXT_COLOR, True),
            (self.wm_text_version, f" | {VERSION} | ", WM_TEXT_COLOR, wm.show_version),
            (self.wm_text_status, f"{st_txt}", st_color, wm.show_status),
            (self.wm_text_suffix, f" | {time.strftime('%H:%M:%S')}", WM_TEXT_COLOR, wm.show_time),
            (self.wm_text_cpu, cpu_str, cpu_color, wm.show_cpu),
            (self.wm_text_gpu, gpu_str, gpu_color, wm.show_gpu),
            (self.wm_text_ram, ram_str, ram_color, wm.show_ram),
            (self.wm_text_ping, ping_str, ping_color, wm.show_ping),
        ]

        # Обновляем canvas-элементы и считаем суммарную ширину
        total_w = 0
        widths = []
        for item, text, color, visible in segments:
            if visible:
                self.canvas.itemconfig(
                    item, text=text, fill=color, state="normal")
                w = self._w(text)
            else:
                self.canvas.itemconfig(item, text="", state="hidden")
                w = 0
            widths.append(w)
            total_w += w

        # ── Размер и позиция фона ─────────────────────────────────
        rect_w = total_w + WM_PAD_X * 2
        rect_h = self._text_h + WM_PAD_Y * 2

        x1, y1 = self._calc_position(rect_w, rect_h)
        x2, y2 = x1 + rect_w, y1 + rect_h

        self.canvas.coords(self.wm_bg, x1, y1, x2, y2)
        self.canvas.itemconfig(self.wm_bg, state="normal")

        self.canvas.coords(self.wm_header, x1, y1, x2, y1 + WM_HEADER_H)
        self.canvas.itemconfig(self.wm_header, fill=self._header_color(), state="normal")

        # ── Расстановка текстов слева направо ─────────────────────
        cx, ty = x1 + WM_PAD_X, y1 + WM_PAD_Y
        for (item, _, _, visible), w in zip(segments, widths):
            if visible:
                self.canvas.coords(item, cx, ty)
                cx += w


# Экземпляр класса MasterOverlay для импорта в меню
overlay_instance = MasterOverlay()
