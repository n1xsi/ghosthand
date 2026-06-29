import dearpygui.dearpygui as dpg

from scripts.aimpull import aimpull_instance
from scripts.anti_aim import anti_aim_instance
from scripts.antiafk import antiafk_instance
from scripts.autopistol import autopistol_instance
from scripts.bunnyhop import bhop_instance
from scripts.fastzoom import fastzoom_instance
from scripts.mrc import mrc_instance
from scripts.panic import panic_instance
from scripts.pixel_triggerbot import pixel_trigger_instance
from scripts.snaptap import snap_tap_instance
from scripts.turn180 import turn180_instance

from src.config import BASE_VIEWPORT_WIDTH, BASE_VIEWPORT_HEIGHT, UI_SCALE
from src.ui.gui import build_gui
from src.ui import theme as theme_module
from src.ui.overlay import overlay_instance
from src.core.sysmon import sysmon

_SCRIPTS = [
    bhop_instance,
    mrc_instance,
    autopistol_instance,
    antiafk_instance,
    pixel_trigger_instance,
    snap_tap_instance,
    aimpull_instance,
    anti_aim_instance,
    fastzoom_instance,
    turn180_instance,
]

if __name__ == "__main__":
    dpg.create_context()
    build_gui()
    theme_module.apply_preset("GhostHand")
    dpg.set_global_font_scale(UI_SCALE)

    dpg.create_viewport(
        title="ghosthand",
        width=BASE_VIEWPORT_WIDTH,
        height=BASE_VIEWPORT_HEIGHT,
        resizable=False,
        decorated=True,
    )

    try:
        dpg.set_viewport_small_icon("assets/icon.ico")
        dpg.set_viewport_large_icon("assets/icon.ico")
    except Exception as e:
        print(f"[debug-UI] Иконка не загружена: {e}")

    dpg.setup_dearpygui()

    for script in _SCRIPTS:
        script.start()

    panic_instance.start()
    overlay_instance.start()
    sysmon.start()

    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
