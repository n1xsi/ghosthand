import dearpygui.dearpygui as dpg

from src.config import DEEP_PURPLE, ACTIVE_PURPLE


def create_theme() -> int:
    """Создаёт и возвращает глобальную тему DearPyGui."""
    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvAll):
            # Окно
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 6)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (20, 20, 20, 255))

            # Чекбоксы
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, DEEP_PURPLE)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (60, 60, 60, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (80, 80, 80, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (90, 90, 90, 255))

            # Вкладки
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, DEEP_PURPLE)
            dpg.add_theme_color(dpg.mvThemeCol_Tab, (54, 0, 102, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, ACTIVE_PURPLE)

            # Слайдеры
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, DEEP_PURPLE)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, ACTIVE_PURPLE)

    return theme
