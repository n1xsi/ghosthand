import ctypes
import time

# ИЗОЛЯЦИЯ
# Вместо глобального ctypes.windll.user32, создание независимой копии
# (чтобы правила из snaptap.py сюда не добрались)
user32 = ctypes.WinDLL('user32')
SendInput = user32.SendInput

# Отключение строгой проверки типов для этой локальной копии
SendInput.argtypes = None

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


# DirectInput Scan Codes
INPUT_MOUSE = 0
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
WH_MOUSE_LL = 14
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
DIK_SPACE = 0x39  # Скан-код пробела
VK_SPACE = 0x20  # Код виртуальной клавиши для проверки удержания (GetAsyncKeyState)
VK_LBUTTON = 0x01
MOUSEEVENTF_MOVE = 0x0001

# Тип для callback-функции хука
HOOKPROC = ctypes.WINFUNCTYPE(
    ctypes.c_long,
    ctypes.c_int,
    ctypes.wintypes.WPARAM,
    ctypes.wintypes.LPARAM
)


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    # 0x0008: KEYEVENTF_SCANCODE
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    # 0x0008 | 0x0002: KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ClickKey(hexKeyCode, delay=0.015):
    PressKey(hexKeyCode)
    time.sleep(delay)
    ReleaseKey(hexKeyCode)

# Функция проверки физического нажатия (для триггера)
def is_key_pressed(vk_code):
    # 0x8000 - это маска "нажата в данный момент"
    return (ctypes.windll.user32.GetAsyncKeyState(vk_code) & 0x8000) != 0


def MouseLeftClick(delay=0.01):
    """Имитирует нажатие левой кнопки мыши"""
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()

    # Отправляем DOWN
    ii_.mi = MouseInput(0, 0, 0, MOUSEEVENTF_LEFTDOWN,
                        0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(INPUT_MOUSE), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    time.sleep(delay)

    # Отправляем UP
    ii_.mi = MouseInput(0, 0, 0, MOUSEEVENTF_LEFTUP, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(INPUT_MOUSE), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def MouseMove(dx, dy):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()

    ii_.mi = MouseInput(int(dx), int(
        dy), 0, MOUSEEVENTF_MOVE, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(INPUT_MOUSE), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
