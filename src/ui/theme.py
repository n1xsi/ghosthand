"""
Система тем GhostHand.

apply_preset(name)   - применить именованный пресет
apply_colors(colors) - применить кастомный набор цветов

При каждой смене темы:
  1. Создаётся новый DPG-объект темы
  2. Привязывается глобально через dpg.bind_theme()
  3. Старый объект удаляется (экономия памяти)
  4. Обновляются теги текстовых элементов GUI
"""
import dearpygui.dearpygui as dpg

from src.config import (
    ThemeColors,
    THEME_PRESETS,
    THEMED_TITLE_TAGS,
    THEMED_HEADER_TAGS,
)

_active_theme_id: int | None = None
_current_colors: ThemeColors | None = None


def get_current_colors() -> ThemeColors | None:
    """Возвращает последний применённый набор цветов (нужен для overlay при сбросе rainbow)."""
    return _current_colors


# ── Внутренние ────────────────────────────────────────────────────
def _lighten(color: tuple, amount: int = 20) -> tuple:
    """Чуть осветляет RGB-цвет (для FrameBgHovered / FrameBgActive)."""
    r, g, b, a = color
    return (min(255, r + amount), min(255, g + amount), min(255, b + amount), a)


def _build_theme(colors: ThemeColors) -> int:
    """Создаёт DPG-объект темы из словаря цветов, возвращает его ID."""
    accent = colors["accent"]
    accent_hover = colors["accent_hover"]
    tab = colors["tab"]
    window_bg = colors["window_bg"]
    frame_bg = colors["frame_bg"]

    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 6)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,  4)

            # Фон окна
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, window_bg)

            # Чекбоксы / поля ввода
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, accent)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, frame_bg)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, _lighten(frame_bg, 20))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, _lighten(frame_bg, 35))

            # Вкладки
            dpg.add_theme_color(dpg.mvThemeCol_Tab, tab)
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, accent_hover)
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, accent)

            # Слайдеры
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, accent)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, accent_hover)

            # Кнопки
            dpg.add_theme_color(dpg.mvThemeCol_Button, tab)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, accent_hover)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, accent)

    return theme


def _update_text_tags(colors: ThemeColors) -> None:
    """Обновляет цвет текстовых элементов GUI под новую тему."""
    for tag in THEMED_TITLE_TAGS:
        if dpg.does_item_exist(tag):
            dpg.configure_item(tag, color=colors["accent"])

    for tag in THEMED_HEADER_TAGS:
        if dpg.does_item_exist(tag):
            dpg.configure_item(tag, color=colors["text_accent"])


# ── Публичный API ─────────────────────────────────────────────────

def apply_colors(colors: ThemeColors) -> None:
    """Применяет произвольный набор цветов как глобальную тему."""
    global _active_theme_id, _current_colors

    new_id = _build_theme(colors)
    dpg.bind_theme(new_id)

    if _active_theme_id is not None and dpg.does_item_exist(_active_theme_id):
        dpg.delete_item(_active_theme_id)
    _active_theme_id = new_id
    _current_colors = colors

    _update_text_tags(colors)


def apply_preset(name: str) -> None:
    """Применяет именованный пресет из THEME_PRESETS."""
    if name not in THEME_PRESETS:
        print(f"[debug:theme] Пресет '{name}' не найден")
        return
    apply_colors(THEME_PRESETS[name])
    print(f"[debug:theme] Тема → {name}")
