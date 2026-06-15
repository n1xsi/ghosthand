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
THEMED_TITLE_TAGS = ["title_text", "wm_title"]
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
]

# ── Алиасы на дефолтную тему (GhostHand) для инициализации GUI ────
DEEP_PURPLE = THEME_PRESETS["GhostHand"]["accent"]
ACTIVE_PURPLE = THEME_PRESETS["GhostHand"]["accent_hover"]
SOFT_PURPLE = THEME_PRESETS["GhostHand"]["text_accent"]
ADDITIONAL_BLACK = (150, 150, 150, 200)

# ── Размеры окна ──────────────────────────────────────────────────
BASE_VIEWPORT_WIDTH = 600
BASE_VIEWPORT_HEIGHT = 420
BASE_STATUS_TEXT_POS = (440, 8)
STATUS_RIGHT_MARGIN = 160

UI_SCALE = 1.4
VERSION = "v0.9.9 Dev Build"
