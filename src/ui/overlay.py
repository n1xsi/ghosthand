from scripts.watermark import watermark_instance
from scripts.aimpull import aimpull_instance
from src.core import input_sim

import tkinter as tk
import threading
import ctypes
import time

WS_EX_TRANSPARENT = 0x00000020
GWL_EXSTYLE = -20


class MasterOverlay:
    def __init__(self):
        self.running = False
        self.root = None
        self.canvas = None

        # Объекты графики
        self.circle_id = None
        self.wm_bg = None
        self.wm_header = None
        # Три объекта текста вместо одного для мульти-цвета
        self.wm_text_prefix = None
        self.wm_text_status = None
        self.wm_text_suffix = None

        # Переменные для реального разрешения
        self.screen_width = 0
        self.screen_height = 0

    def start(self):
        self.running = True
        threading.Thread(target=self._run_tk, daemon=True).start()

    def _run_tk(self):
        try:
            # ФИКС DPI:
            # Чтобы программа игнорировала масштаб Windows (125%, 150%, ...)
            # Гарантия того, что 1 пиксель Ткинтера = 1 физический пиксель монитора
            ctypes.windll.user32.SetProcessDPIAware()

            self.root = tk.Tk()

            # Окно без рамок
            self.root.overrideredirect(True)
            # Поверх всех окон
            self.root.wm_attributes("-topmost", True)
            # Прозрачная маска (чёрный цвет)
            self.root.wm_attributes("-transparentcolor", "black")
            self.root.config(bg="black")

            # Получение реального разрешения экрана через WinAPI
            self.screen_width = ctypes.windll.user32.GetSystemMetrics(0)
            self.screen_height = ctypes.windll.user32.GetSystemMetrics(1)

            # Растягивание окна на реальный размер экрана
            self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")

            # Применение к окну "проницания" для кликов (Click-Through)
            self.root.update_idletasks()
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())

            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_TRANSPARENT)

            # Создние холста
            self.canvas = tk.Canvas(
                self.root,
                width=self.screen_width,
                height=self.screen_height,
                bg='black',
                bd=0,
                highlightthickness=0,
                relief='ridge'
            )
            # Заполнение всего холста без отступов
            self.canvas.pack(fill='both', expand=True)

            # ----- СОЗДАНИЕ ОБЪЕКТОВ ГРАФИКИ -----
            # FOV circle
            self.circle_id = self.canvas.create_oval(0, 0, 0, 0, outline="white", width=2)
            # Watermark 1/2 (Фон и Шапка)
            self.wm_bg = self.canvas.create_rectangle(0, 0, 0, 0, fill="#1A1A1A", outline="#333333", width=1)
            self.wm_header = self.canvas.create_rectangle(0, 0, 0, 0, fill="#8B00FF", outline="")  # 8B00FF = DEEP_PURPLE
            
            # Watermark 2/2 (Тексты)
            font_settings = ("Consolas", 10, "bold")
            self.wm_text_prefix = self.canvas.create_text(0, 0, text="", fill="white", font=font_settings, anchor="nw")
            self.wm_text_status = self.canvas.create_text(0, 0, text="", fill="white", font=font_settings, anchor="nw")
            self.wm_text_suffix = self.canvas.create_text(0, 0, text="", fill="white", font=font_settings, anchor="nw")

            print(f"[debug:overlay] Master Overlay initialized. True Resolution: {self.screen_width}x{self.screen_height}")
            self.update_loop()
            self.root.mainloop()

        except Exception as e:
            print(f"[debug:overlay] Failed to start UI: {e}")

    def update_loop(self):
        if not self.running:
            self.root.destroy()
            return

        try:
            # ---------------- FOV CIRCLE ----------------
            if aimpull_instance.show_fov and aimpull_instance.enabled:
                fov = aimpull_instance.fov
                center_x, center_y = self.screen_width // 2, self.screen_height // 2
                self.canvas.coords(self.circle_id, center_x - fov, center_y - fov, center_x + fov, center_y + fov)
                self.canvas.itemconfig(self.circle_id, outline=aimpull_instance.fov_color, state='normal')
            else:
                self.canvas.itemconfig(self.circle_id, state='hidden')

            # ---------------- WATERMARK ----------------
            if watermark_instance.enabled:
                # Формирование ТРИ части текста
                prefix_str = "GHOSTHAND | v0.9.8 Dev Build | "

                if input_sim.GLOBAL_PAUSE:
                    status_str = "GLOBAL PAUSE"
                    status_color = "#FF6B6B"  # Бледно-красный
                else:
                    status_str = "SYSTEM ACTIVE"
                    status_color = "#55FF88"  # Бледно-зелёный

                suffix_str = f" | {time.strftime('%H:%M:%S')}"

                # Обновление текстов и цвета
                self.canvas.itemconfig(self.wm_text_prefix, text=prefix_str, state='normal')
                self.canvas.itemconfig(self.wm_text_status, text=status_str, fill=status_color, state='normal')
                self.canvas.itemconfig(self.wm_text_suffix, text=suffix_str, state='normal')

                # Высчитывание ширины каждого блока для конкатенации
                bbox_p = self.canvas.bbox(self.wm_text_prefix)
                bbox_s = self.canvas.bbox(self.wm_text_status)
                bbox_su = self.canvas.bbox(self.wm_text_suffix)

                w_p = bbox_p[2] - bbox_p[0]
                w_s = bbox_s[2] - bbox_s[0]
                w_su = bbox_su[2] - bbox_su[0]

                text_h = bbox_p[3] - bbox_p[1]  # Высота шрифта
                total_text_w = w_p + w_s + w_su

                # Отступы и позиционирование
                pad_x, pad_y = 10, 6
                rect_w = total_text_w + (pad_x * 2)
                rect_h = text_h + (pad_y * 2)

                x1 = self.screen_width - rect_w - 20
                y1 = 20
                x2 = x1 + rect_w
                y2 = y1 + rect_h

                # Отрисовка Фона и Шапки
                self.canvas.coords(self.wm_bg, x1, y1, x2, y2)
                self.canvas.itemconfig(self.wm_bg, state='normal')

                self.canvas.coords(self.wm_header, x1, y1, x2, y1 + 2)
                self.canvas.itemconfig(self.wm_header, state='normal')

                # Постановка текстов в одну линию с отступами
                start_x = x1 + pad_x
                self.canvas.coords(self.wm_text_prefix, start_x, y1 + pad_y)
                self.canvas.coords(self.wm_text_status, start_x + w_p, y1 + pad_y)
                self.canvas.coords(self.wm_text_suffix, start_x + w_p + w_s, y1 + pad_y)

            else:
                self.canvas.itemconfig(self.wm_bg, state='hidden')
                self.canvas.itemconfig(self.wm_header, state='hidden')
                self.canvas.itemconfig(self.wm_text_prefix, state='hidden')
                self.canvas.itemconfig(self.wm_text_status, state='hidden')
                self.canvas.itemconfig(self.wm_text_suffix, state='hidden')

        except Exception as e:
            print(f"[debug:overlay] Update loop crashed: {e}")

        # Цикл обновления
        self.root.after(16, self.update_loop)


# Экземпляр класса MasterOverlay для импорта в меню
overlay_instance = MasterOverlay()
