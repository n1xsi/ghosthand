import threading
import ctypes
import ctypes.wintypes
import traceback

# ─── Константы ──────────────────────────────────────────────
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002

VK_A = 0x41
VK_D = 0x44
SCAN_A = 0x1E
SCAN_D = 0x20

EXTRA_MARKER = 0x5441

# ─── ctypes-структуры ──────────────────────────────────────
user32 = ctypes.windll.user32


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk",         ctypes.wintypes.WORD),
        ("wScan",       ctypes.wintypes.WORD),
        ("dwFlags",     ctypes.wintypes.DWORD),
        ("time",        ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_void_p),
    ]

# ЭТУ СТРУКТУРУ НЕ УДАЛЯТЬ! Нужна для правильного размера памяти Union
# Без неё нихера не работает крч
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx",          ctypes.c_long),
        ("dy",          ctypes.c_long),
        ("mouseData",   ctypes.wintypes.DWORD),
        ("dwFlags",     ctypes.wintypes.DWORD),
        ("time",        ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_void_p),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg",    ctypes.wintypes.DWORD),
        ("wParamL", ctypes.wintypes.WORD),
        ("wParamH", ctypes.wintypes.WORD),
    ]


class _INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    ]


class INPUT(ctypes.Structure):
    _fields_ = [
        ("type",  ctypes.wintypes.DWORD),
        ("union", _INPUT_UNION),
    ]


class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode",      ctypes.wintypes.DWORD),
        ("scanCode",    ctypes.wintypes.DWORD),
        ("flags",       ctypes.wintypes.DWORD),
        ("time",        ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_void_p),
    ]


HOOKPROC = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_int, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM)

user32.SetWindowsHookExW.argtypes = [ctypes.c_int, HOOKPROC, ctypes.wintypes.HINSTANCE, ctypes.wintypes.DWORD]
user32.SetWindowsHookExW.restype = ctypes.c_void_p

user32.CallNextHookEx.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM]
user32.CallNextHookEx.restype = ctypes.c_long

user32.SendInput.argtypes = [ctypes.c_uint, ctypes.POINTER(INPUT), ctypes.c_int]
user32.SendInput.restype = ctypes.c_uint


# ─── Логика Snap Tap ───────────────────────────────────────
class SnapTapCore:
    def __init__(self):
        self.running = False
        self.enabled = False

        self.is_a_pressed = False
        self.is_d_pressed = False
        self.hook_handle = None
        self.c_callback = None

    def start(self):
        self.running = True
        threading.Thread(target=self._hook_thread, daemon=True).start()

    def _send_key(self, vk: int, scan: int, up: bool = False):
        flags = 0 if not up else KEYEVENTF_KEYUP
        ki = KEYBDINPUT(wVk=vk, wScan=scan, dwFlags=flags,
                        time=0, dwExtraInfo=EXTRA_MARKER)

        inp = INPUT()
        inp.type = INPUT_KEYBOARD
        inp.union.ki = ki

        # Если SendInput возвращает 0, значит произошла ошибка на уровне Windows
        res = user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))
        if res == 0:
            print("[debug:SnapTap] SendInput failed!")

    def _hook_thread(self):
        # ОПРЕДЕЛЯЕНИЕ ФУНКЦИИ ВНУТРИ ПОТОКА
        # Это решает проблему с 'self', чтобы сигнатура принимала ровно 3 аргумента
        def keyboard_proc(nCode, wParam, lParam):
            try:
                if nCode < 0:
                    return user32.CallNextHookEx(self.hook_handle, nCode, wParam, lParam)

                kb = ctypes.cast(lParam, ctypes.POINTER(
                    KBDLLHOOKSTRUCT)).contents
                vk = kb.vkCode

                # Пропускаем наши симуляции
                # В Python 64-bit значения dwExtraInfo могут кастоваться криво,
                # поэтому надежнее проверить оба варианта каста
                if kb.dwExtraInfo == EXTRA_MARKER or kb.dwExtraInfo == getattr(ctypes.c_void_p(EXTRA_MARKER), 'value', None):
                    return user32.CallNextHookEx(self.hook_handle, nCode, wParam, lParam)

                # Если выключен
                if not self.enabled:
                    self.is_a_pressed = False
                    self.is_d_pressed = False
                    return user32.CallNextHookEx(self.hook_handle, nCode, wParam, lParam)

                # ── A ───────────────────────────────────────────────────
                if vk == VK_A:
                    if wParam == WM_KEYDOWN:
                        if not self.is_a_pressed:
                            self.is_a_pressed = True
                            if self.is_d_pressed:
                                self._send_key(VK_D, SCAN_D, up=True)
                            self._send_key(VK_A, SCAN_A, up=False)
                        return 1

                    elif wParam == WM_KEYUP:
                        self.is_a_pressed = False
                        self._send_key(VK_A, SCAN_A, up=True)
                        if self.is_d_pressed:
                            self._send_key(VK_D, SCAN_D, up=False)
                        return 1

                # ── D ───────────────────────────────────────────────────
                elif vk == VK_D:
                    if wParam == WM_KEYDOWN:
                        if not self.is_d_pressed:
                            self.is_d_pressed = True
                            if self.is_a_pressed:
                                self._send_key(VK_A, SCAN_A, up=True)
                            self._send_key(VK_D, SCAN_D, up=False)
                        return 1

                    elif wParam == WM_KEYUP:
                        self.is_d_pressed = False
                        self._send_key(VK_D, SCAN_D, up=True)
                        if self.is_a_pressed:
                            self._send_key(VK_A, SCAN_A, up=False)
                        return 1

            except Exception as e:
                print(f"[debug:SnapTap] Error in hook: {e}")
                traceback.print_exc()

            return user32.CallNextHookEx(self.hook_handle, nCode, wParam, lParam)

        self.c_callback = HOOKPROC(keyboard_proc)
        self.hook_handle = user32.SetWindowsHookExW(
            WH_KEYBOARD_LL, self.c_callback, None, 0)

        if not self.hook_handle:
            print("[debug:SnapTap] Failed to install Snap Tap hook!")
            return

        msg = ctypes.wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

# Экземпляр класса SnapTapCore для импорта в меню
snap_tap_instance = SnapTapCore()
