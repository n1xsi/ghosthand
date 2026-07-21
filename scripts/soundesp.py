"""
Sound ESP (Offscreen Arrows).

Рисует стрелки по кругу от прицела в сторону, откуда пришёл звук.
Источник данных: системный микс через WASAPI loopback (src/core/audio_cap.py).
Память игры не читается, в процесс ничего не внедряется.

Ограничения:
- Это ПЕЛЕНГ, а не позиция: ни дистанции, ни высоты.
- Ось перед/зад достоверна только на дискретных 5.1/7.1 endpoint'ах.
На стерео она оценивается по тембру (глухой звук = сзади) - стрелка
в этом случае красится серым (SE_UNSURE_COLOR).
"""
from src.config import (
    SE_RADIUS, SE_SIZE, SE_DECAY, SE_SENSITIVITY, SE_COLOR, SE_MAX_ARROWS,
    SE_UNSURE_DIM, SE_TRUST_CONF, SE_MERGE_DEG,
)
from src.core import audio_cap
from src.core.audio_cap import audio_capture
from src.core.base import ScriptBase


class SoundEspCore(ScriptBase):
    """
    Настройки + прокси к сервису захвата.

    Своего потока не держит: аудио-поток живёт в audio_capture, а оверлей
    сам опрашивает active_arrows() на каждом кадре. start()/_loop() из
    ScriptBase переопределены — крутить пустой цикл незачем.
    """

    def __init__(self) -> None:
        super().__init__()

        self.radius = SE_RADIUS
        self.size = SE_SIZE
        self.decay = SE_DECAY
        self.sensitivity = SE_SENSITIVITY
        self.color = SE_COLOR
        self.footstep_filter = True  # Полоса 200-2000 Гц вместо всего спектра
        self.reject_own = True       # Глушить всенаправленное (свой выстрел, музыка)

    # ── Жизненный цикл ────────────────────────────────────────────
    def start(self) -> None:
        """Поток не нужен: захват стартует лениво при первом включении."""
        self.running = True

    def set_enabled(self, value: bool) -> None:
        """Аудио-поток крутится только когда функция реально включена."""
        self.enabled = value
        if value:
            audio_capture.start()
        else:
            audio_capture.stop()

    # ── Проброс настроек в детектор ────────────────────────────────
    def apply_tuning(self) -> None:
        audio_cap.RISE_DB = self.sensitivity
        audio_cap.MIN_CONFIDENCE = 0.30 if self.reject_own else 0.0
        if self.footstep_filter:
            audio_cap.BAND_LO_HZ, audio_cap.BAND_HI_HZ = 200.0, 2000.0
        else:
            audio_cap.BAND_LO_HZ, audio_cap.BAND_HI_HZ = 40.0, 16000.0

    # ── Данные для оверлея ────────────────────────────────────────
    @staticmethod
    def _angular_gap(a: float, b: float) -> float:
        """Угловое расстояние по кратчайшей дуге, 0..180°."""
        d = abs(a - b) % 360.0
        return 360.0 - d if d > 180.0 else d

    def active_arrows(self) -> list[tuple[float, float, bool]]:
        """
        [(угол°, яркость 0..1, достоверна ли ось перед/зад)].

        Ранжируем по intensity * confidence, а НЕ по одной громкости.
        Замер: с выключенным reject_own всенаправленная музыка давала
        события яркости 0.65 против 0.20 у реальных шагов и вытесняла их
        из SE_MAX_ARROWS слотов — на экране оставался мусор. Пеленг без
        направленности бесполезен, поэтому он идёт вниз списка и гасится.
        """
        if not self.enabled:
            return []

        # В стерео потолок доверия ниже, иначе любая стерео-стрелка считалась бы недостоверной
        ceiling = audio_cap.STEREO_CONFIDENCE if audio_capture.mode == "stereo" else 1.0

        scored = []
        for e in audio_capture.recent(self.decay):
            fade = 1.0 - (e.age() / self.decay)
            if fade <= 0.0:
                continue

            trust = min(1.0, e.confidence / ceiling) if ceiling > 0 else 0.0
            directional = trust >= SE_TRUST_CONF

            bright = e.intensity * fade
            if not directional:
                bright *= SE_UNSURE_DIM  # Пеленга по сути нет - не отвлекаем ярким

            # Сортировка по "полезности", а не по громкости
            scored.append((bright * max(trust, 0.05), e.angle, bright,
                           e.fb_known and directional))

        scored.sort(key=lambda x: x[0], reverse=True)

        # Одно событие часто бьётся на несколько блоков - схлопываем близкие
        # пеленги, иначе один шаг съедает все слоты веером стрелок
        out: list[tuple[float, float, bool]] = []
        for _, angle, bright, fb_known in scored:
            if any(self._angular_gap(angle, prev) < SE_MERGE_DEG for prev, _, _ in out):
                continue
            out.append((angle, bright, fb_known))
            if len(out) >= SE_MAX_ARROWS:
                break
        return out

    # ── Выбор устройства ──────────────────────────────────────────
    AUTO_DEVICE = "Auto (first live endpoint)"

    def device_choices(self) -> list[str]:
        """Пункты комбо-бокса. Виртуальные помечены - их loopback часто нем."""
        items = [self.AUTO_DEVICE]
        try:
            for name, ch, virt in audio_capture.list_devices():
                items.append(f"{ch}ch  {name}" + ("  [virtual]" if virt else ""))
        except Exception as exc:
            items.append(f"(enumeration failed: {exc})")
        return items

    def set_device(self, label: str) -> None:
        """Обратный разбор пункта комбо-бокса в имя endpoint'а."""
        if label == self.AUTO_DEVICE or label.startswith("("):
            audio_capture.preferred_device = ""
        else:
            name = label.split("ch  ", 1)[-1]
            audio_capture.preferred_device = name.replace("  [virtual]", "")

        # Перезапуск: устройство выбирается при входе в сессию записи
        if self.enabled:
            audio_capture.stop()
            audio_capture.start()

    # ── Строка состояния для UI ───────────────────────────────────
    def status_line(self) -> str:
        if not self.enabled:
            return "Disabled"
        mode = audio_capture.mode
        if mode == "off":
            return audio_capture.status
        axis = "360 bearing" if mode == "surround" else "L/R + timbre guess"
        return f"{audio_capture.channels}ch {mode} - {axis}"

    def device_line(self) -> str:
        return audio_capture.device_name or "(searching...)"

    def level_line(self) -> str:
        """Текущий уровень в полосе + порог: по этой строке крутят Threshold."""
        if not self.enabled or audio_capture.mode == "off":
            return "-"
        return f"{audio_capture.level_db:+.0f} dB   (needs +{self.sensitivity:.0f} over background)"


# Экземпляр класса SoundEspCore для импорта в меню
soundesp_instance = SoundEspCore()
