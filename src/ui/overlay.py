from scripts.aimpull import aimpull_instance
import tkinter as tk
import threading
import ctypes

WS_EX_TRANSPARENT = 0x00000020
GWL_EXSTYLE = -20


class FovOverlay:
    def __init__(self):
        self.running = False
        self.root = None
        self.canvas = None
        self.circle_id = None

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

            self.root.overrideredirect(True)                       # Окно без рамок
            self.root.wm_attributes("-topmost", True)              # Поверх всех окон
            self.root.wm_attributes("-transparentcolor", "black")  # Прозрачная маска (чёрный цвет)
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

            # Создание круга (FOV circle)
            self.circle_id = self.canvas.create_oval(0, 0, 0, 0, outline="white", width=2)

            print(f"[debug:overlay] FOV Overlay initialized. True Resolution: {self.screen_width}x{self.screen_height}")
            self.update_loop()
            self.root.mainloop()

        except Exception as e:
            print(f"[debug:overlay] Failed to start FOV Overlay: {e}")

    def update_loop(self):
        if not self.running:
            self.root.destroy()
            return

        try:
            if aimpull_instance.show_fov and aimpull_instance.enabled:
                fov = aimpull_instance.fov
                color = aimpull_instance.fov_color

                center_x = self.screen_width // 2
                center_y = self.screen_height // 2

                x0 = center_x - fov
                y0 = center_y - fov
                x1 = center_x + fov
                y1 = center_y + fov

                self.canvas.coords(self.circle_id, x0, y0, x1, y1)
                self.canvas.itemconfig(self.circle_id, outline=color, state='normal')
            else:
                self.canvas.itemconfig(self.circle_id, state='hidden')

        except Exception as e:
            print(f"[debug:overlay] Update loop crashed: {e}")

        # Цикл обновления
        self.root.after(16, self.update_loop)

# Экземпляр класса FovOverlay для импорта в меню
fov_overlay_instance = FovOverlay()
