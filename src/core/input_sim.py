import ctypes
import ctypes.wintypes
import time

# ── Глобальное состояние ──────────────────────────────────────────

# Panic Key - при нажатии останавливает все функции
GLOBAL_PAUSE = False

# Изолированная копия user32 (не трогает глобальный ctypes.windll.user32)
user32 = ctypes.WinDLL('user32')
SendInput = user32.SendInput
SendInput.argtypes = None  # Отключение строгой проверки типов

# ── Константы ─────────────────────────────────────────────────────

# Mouse flags
INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010

# Virtual key codes — мышь
VK_LBUTTON = 0x01    # Левая кнопка мыши
VK_XBUTTON1 = 0x05   # Нижняя боковая кнопка (mouse4)
VK_MIDBUTTON = 0x04  # Средняя кнопка (mouse3)

# Virtual key codes — клавиатура
DIK_Q = 0x10     # Скан-код 'Q'
VK_PAUSE = 0x13  # 'Pause/Break'
DIK_ALT = 0xA4   # 'Left Alt'
VK_F = 0x46      # 'F'
VK_T = 0x54      # 'T'

# ── C-типы ────────────────────────────────────────────────────────

PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk",        ctypes.c_ushort),
        ("wScan",      ctypes.c_ushort),
        ("dwFlags",    ctypes.c_ulong),
        ("time",       ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg",    ctypes.c_ulong),
        ("wParamL", ctypes.c_ushort),
        ("wParamH", ctypes.c_ushort),
    ]


class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx",          ctypes.c_long),
        ("dy",          ctypes.c_long),
        ("mouseData",   ctypes.c_ulong),
        ("dwFlags",     ctypes.c_ulong),
        ("time",        ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class Input_I(ctypes.Union):
    _fields_ = [
        ("ki", KeyBdInput),
        ("mi", MouseInput),
        ("hi", HardwareInput),
    ]


class Input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ii",   Input_I),
    ]


class POINT(ctypes.Structure):
    """Координаты курсора (WinAPI POINT)."""
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class KBDLLHOOKSTRUCT(ctypes.Structure):
    """Структура для low-level keyboard hook (используется в SnapTap)."""
    _fields_ = [
        ("vkCode",      ctypes.wintypes.DWORD),
        ("scanCode",    ctypes.wintypes.DWORD),
        ("flags",       ctypes.wintypes.DWORD),
        ("time",        ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_void_p),
    ]


# Тип callback-функции для SetWindowsHookEx (__stdcall, как требует WinAPI)
HOOKPROC = ctypes.WINFUNCTYPE(
    ctypes.c_long,
    ctypes.c_int,
    ctypes.wintypes.WPARAM,
    ctypes.wintypes.LPARAM
)


# ── Функции ───────────────────────────────────────────────────────
def PressKey(hexKeyCode: int) -> None:
    """Нажатие клавиши по scan-коду."""
    if GLOBAL_PAUSE:
        return
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode: int) -> None:
    """Отпускание клавиши по scan-коду."""
    if GLOBAL_PAUSE:
        return
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ClickKey(hexKeyCode: int, delay: float = 0.015) -> None:
    """Нажатие + отпускание клавиши с задержкой."""
    if GLOBAL_PAUSE:
        return
    PressKey(hexKeyCode)
    time.sleep(delay)
    ReleaseKey(hexKeyCode)


def is_key_pressed(vk_code: int) -> bool:
    """Возвращает True, если клавиша зажата прямо сейчас."""
    if GLOBAL_PAUSE:
        return False
    return (ctypes.windll.user32.GetAsyncKeyState(vk_code) & 0x8000) != 0


def MouseClick(
    delay: float = 0.01,
    m_down: int = MOUSEEVENTF_LEFTDOWN,
    m_up: int = MOUSEEVENTF_LEFTUP,
) -> None:
    """Имитирует клик кнопкой мыши (down → sleep → up)."""
    if GLOBAL_PAUSE:
        return
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()

    # Отправка DOWN
    ii_.mi = MouseInput(0, 0, 0, m_down, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(INPUT_MOUSE), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    time.sleep(delay)

    # Отправка UP
    ii_.mi = MouseInput(0, 0, 0, m_up, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(INPUT_MOUSE), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def MouseMove(dx: int, dy: int) -> None:
    """Относительное перемещение мыши на (dx, dy) пикселей."""
    if GLOBAL_PAUSE:
        return
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(int(dx), int(dy), 0, MOUSEEVENTF_MOVE, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(INPUT_MOUSE), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
