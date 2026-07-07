from src.config import WM_DEFAULT_POSITION, UI_SCALE


class WatermarkCore:
    def __init__(self):
        self.enabled = False
        self.rainbow = False
        self.position = WM_DEFAULT_POSITION
        self.scale = UI_SCALE

        # Что показывать по умолчанию
        self.show_version = True
        self.show_status = True
        self.show_time = True

        # Системный монитор — что показывать
        self.show_cpu = False
        self.show_gpu = False
        self.show_ram = False
        self.show_ping = False


# Экземпляр класса WatermarkCore для импорта в меню
watermark_instance = WatermarkCore()
