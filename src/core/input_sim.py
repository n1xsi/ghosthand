import ctypes
import time

# -------- ПЕРЕМЕННЫЕ --------

# Глобальная пауза
GLOBAL_PAUSE = False

# ИЗОЛЯЦИЯ - вместо глобального "ctypes.windll.user32" создание независимой копии
user32 = ctypes.WinDLL('user32')
SendInput = user32.SendInput

# Отключение строгой проверки типов для этой локальной копии
SendInput.argtypes = None

# -------- КОНСТАНТЫ --------

# Mouse Buttons
INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP   = 0x0010
VK_LBUTTON = 0x01
VK_XBUTTON1 = 0x05  # mouse4

# Keyboard Scan Codes
DIK_Q = 0x10     # Скан-код клавиши Q
VK_PAUSE = 0x13  # Кнопка Pause/Break
DIK_ALT = 0xA4   # Скан-код клавиши Alt
VK_F = 0x46      # Виртуальный код клавиши 'F'

# C type definitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_ushort),
                ("wParamH", ctypes.c_ushort)]


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
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Структура координат курсора
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

# Тип для callback-функции хука
HOOKPROC = ctypes.WINFUNCTYPE(
    ctypes.c_long,
    ctypes.c_int,
    ctypes.wintypes.WPARAM,
    ctypes.wintypes.LPARAM
)


# -------- ФУНКЦИИ --------
def PressKey(hexKeyCode):
    if GLOBAL_PAUSE: return
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    # 0x0008: KEYEVENTF_SCANCODE
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    if GLOBAL_PAUSE: return
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    # 0x0008 | 0x0002: KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ClickKey(hexKeyCode, delay=0.015):
    if GLOBAL_PAUSE: return
    PressKey(hexKeyCode)
    time.sleep(delay)
    ReleaseKey(hexKeyCode)

# Функция проверки физического нажатия
def is_key_pressed(vk_code):
    if GLOBAL_PAUSE: return
    # 0x8000 = "нажата в данный момент"
    return (ctypes.windll.user32.GetAsyncKeyState(vk_code) & 0x8000) != 0


def MouseClick(delay=0.01, m_down=MOUSEEVENTF_LEFTDOWN, m_up=MOUSEEVENTF_LEFTUP):
    if GLOBAL_PAUSE: return
    """Имитирует нажатие левой кнопки мыши"""
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()

    # Отправляем DOWN
    ii_.mi = MouseInput(0, 0, 0, m_down, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(INPUT_MOUSE), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    time.sleep(delay)

    # Отправляем UP
    ii_.mi = MouseInput(0, 0, 0, m_up, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(INPUT_MOUSE), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def MouseMove(dx, dy):
    if GLOBAL_PAUSE: return
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()

    ii_.mi = MouseInput(int(dx), int(dy), 0, MOUSEEVENTF_MOVE, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(INPUT_MOUSE), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
