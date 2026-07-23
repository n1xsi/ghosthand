from typing import TypedDict


class ThemeColors(TypedDict):
    accent:       tuple[int, int, int, int]
    accent_hover: tuple[int, int, int, int]
    tab:          tuple[int, int, int, int]
    window_bg:    tuple[int, int, int, int]
    frame_bg:     tuple[int, int, int, int]
    text_accent:  tuple[int, int, int, int]


THEME_PRESETS: dict[str, ThemeColors] = {
    "GhostHand": {
        "accent":       (139, 0,   255, 255),
        "accent_hover": (184, 102, 255, 255),
        "tab":          (54,  0,   102, 255),
        "window_bg":    (20,  20,  20,  255),
        "frame_bg":     (60,  60,  60,  255),
        "text_accent":  (163, 102, 255, 255),
    },
    "Black & White": {
        "accent":       (210, 210, 210, 255),
        "accent_hover": (255, 255, 255, 255),
        "tab":          (65,  65,  65,  255),
        "window_bg":    (15,  15,  15,  255),
        "frame_bg":     (50,  50,  50,  255),
        "text_accent":  (180, 180, 180, 255),
    },
    "Razer": {
        "accent":       (0,  255, 65,  255),
        "accent_hover": (57, 255, 20,  255),
        "tab":          (0,  70,  20,  255),
        "window_bg":    (10, 10,  10,  255),
        "frame_bg":     (20, 30,  20,  255),
        "text_accent":  (0,  200, 50,  255),
    },
}

# Все GUI-теги, чей цвет обновляется при смене темы
# title_text  → цвет accent
# остальные   → цвет text_accent
THEMED_TITLE_TAGS = ["title_text"]
THEMED_HEADER_TAGS = [
    "header_aimpull",
    "header_trigger",
    "header_autopistol",
    "header_mrc",
    "header_antiaim",
    "header_bhop",
    "header_fastzoom",
    "header_turn180",
    "header_custom_theme",
    "header_theme_label",
    "header_watermark",
    "header_soundesp",
]

# Hex-версия акцентного цвета (tkinter fallback до применения темы)
DEEP_PURPLE_HEX = "#8B00FF"
WM_DEFAULT_POSITION = "Top Right"

# ── Алиасы на дефолтную тему (GhostHand) для инициализации GUI ────
DEEP_PURPLE = THEME_PRESETS["GhostHand"]["accent"]
ACTIVE_PURPLE = THEME_PRESETS["GhostHand"]["accent_hover"]
SOFT_PURPLE = THEME_PRESETS["GhostHand"]["text_accent"]
ADDITIONAL_BLACK = (150, 150, 150, 200)

# ── Watermark overlay ─────────────────────────────────────────────
WM_BG_FILL = "#1A1A1A"        # Фон ватермарки
WM_BG_OUTLINE = "#333333"     # Рамка фона
WM_TEXT_COLOR = "white"         # Цвет основного текста
WM_STATUS_PAUSE = "#FF6B6B"   # Цвет статуса при глобальной паузе
WM_STATUS_ACTIVE = "#55FF88"  # Цвет статуса при активном состоянии
WM_MARGIN = 20                  # Отступ от края экрана (пикс.)
WM_PAD_X = 10                   # Горизонтальный внутренний отступ
WM_PAD_Y = 6                    # Вертикальный внутренний отступ
WM_HEADER_H = 2                 # Высота цветной полосочки шапки (пикс.)
WM_FONT_NAME = "Consolas"       # Шрифт
WM_FONT_BASE = 10               # Базовый размер при UI_SCALE = 1.4
WM_FONT_MIN = 8                 # Минимальный размер шрифта
WM_POSITIONS = [                # Варианты позиции ватермарки
    "Top Left", "Top Center", "Top Right",
    "Bottom Left", "Bottom Center", "Bottom Right",
]

# ── Sound ESP (Offscreen Arrows) ──────────────────────────────────
# Пеленг по системному звуку (WASAPI loopback). Памяти игры не читает.
SE_RADIUS = 190                # Радиус кольца стрелок от центра экрана (пиксели)
SE_RADIUS_MIN = 80
SE_RADIUS_MAX = 500
SE_SIZE = 22                   # Длина стрелки (пиксели)
SE_SIZE_MIN = 10
SE_SIZE_MAX = 60
SE_DECAY = 0.55                # Сколько секунд живёт стрелка после звука
SE_DECAY_MIN = 0.15
SE_DECAY_MAX = 2.0
SE_SENSITIVITY = 6.0           # Порог превышения над фоном (дБ), меньше = чувствительнее
SE_SENS_MIN = 2.0
SE_SENS_MAX = 20.0
SE_COLOR = "#FF3B3B"         # Цвет стрелки на пике
SE_COLOR_FADE = "#4A1010"    # Цвет на исходе затухания
SE_MAX_ARROWS = 6              # Максимум одновременных стрелок
SE_ARROW_SLOTS = 8             # Сколько polygon-объектов держим в пуле canvas
SE_UNSURE_COLOR = "#8A8A8A"  # Цвет, когда ось перед/зад недостоверна
SE_MIN_INTENSITY = 0.08        # Ниже - не рисуем вовсе
SE_UNSURE_DIM = 0.35           # Множитель яркости для всенаправленного звука (пеленга нет)
SE_TRUST_CONF = 0.50           # Ниже этой доли от потолка — стрелка серая
SE_MERGE_DEG = 12.0            # Стрелки ближе этого угла сливаются в одну


CPU_WARN_THRESHOLD = 80    # %
GPU_WARN_THRESHOLD = 80    # %
RAM_WARN_THRESHOLD  = 85   # %
PING_WARN_THRESHOLD = 100  # мс
WM_WARN_COLOR = WM_STATUS_PAUSE  # Тот же красный, что и GLOBAL PAUSE

# ── Размеры окна ──────────────────────────────────────────────────
BASE_VIEWPORT_WIDTH = 600
BASE_VIEWPORT_HEIGHT = 420
BASE_STATUS_TEXT_POS = (440, 8)
STATUS_RIGHT_MARGIN = 160
UI_SCALE = 1.4

VERSION = "v0.9.9 Dev Build"
