"""
Захват системного звука (WASAPI loopback) для Sound ESP.

Фоновый сервис по образцу sysmon.py: поток пишет в поля экземпляра,
потребители (скрипт/оверлей) читают их без блокировок.

Замеры на реальном железе:
- Виртуальные surround-устройства (Razer Surround, Windows Sonic) отдают
loopback-тишину. Снимать надо с физического endpoint'а, поэтому тут
есть авто-фолбэк по "живости", а не просто default_speaker().
- Физический endpoint обычно двухканальный (2ch) => дискретных FL/FR/BL/BR
нет. Перед/зад тогда оценивается по спектру (глухой звук = сзади), а не
по каналам, и уверенность этой оси считается отдельно...
"""
from __future__ import annotations

import ctypes
import math
import threading
import time
from collections import deque

import numpy as np

SAMPLERATE = 48000
BLOCK = 1024  # ~21 мс при 48 кГц

# Раскладка каналов WASAPI (порядок фиксирован спецификацией)
LAYOUTS: dict[int, list[str]] = {
    1: ["FC"],
    2: ["FL", "FR"],
    4: ["FL", "FR", "BL", "BR"],
    6: ["FL", "FR", "FC", "LFE", "BL", "BR"],
    8: ["FL", "FR", "FC", "LFE", "BL", "BR", "SL", "SR"],
}

# Пеленг: 0° = прямо перед игроком, + = вправо, ±180° = за спиной
CHANNEL_ANGLES: dict[str, float | None] = {
    "FL": -45.0, "FR": 45.0,
    "FC": 0.0, "LFE": None,  # None: сабвуфер не несёт направления
    "BL": -135.0, "BR": 135.0,
    "SL": -90.0, "SR": 90.0,
}

# ── Тюнинги детектора (миграция в src/config.py при подключении UI) ──
BAND_LO_HZ = 200.0        # Полоса шагов/перезарядки
BAND_HI_HZ = 2000.0
TILT_LO_HZ = 300.0        # Полосы для спектрального наклона (перед/зад)
TILT_HI_HZ = 2000.0
TILT_HI2_HZ = 12000.0
RISE_DB = 6.0             # Насколько блок должен выпрыгнуть над фоном
FLOOR_DB = -70.0          # Абсолютный порог тишины
COOLDOWN_S = 0.12         # Один шаг = одна стрелка
BASELINE_BLOCKS = 40      # ~0.85 с фона
BASELINE_MIN = 12         # Пока фон не набран - только учимся, событий не выдаём
MIN_CONFIDENCE = 0.30     # Ниже - считаем звук всенаправленным (свой выстрел/музыка)
STEREO_CONFIDENCE = 0.60  # Потолок доверия для 2ch (L/R достоверен, перед/зад - оценка)
TILT_MARGIN_DB = 4.0      # Разница наклона, считающаяся уверенным «сзади»

# Виртуальные endpoint'ы: их loopback может отдавать тишину
VIRTUAL_HINTS = (
    "surround", "sonic", "atmos", "nvidia", "virtual",
    "steam", "voicemeeter", "vb-audio", "cable",
)
SILENCE_SWITCH_S = 3.0  # Столько bit-exact тишины => пробуем следующий endpoint

# COM-апартамент нужен КАЖДОМУ потоку, который трогает WASAPI
# soundcard делает CoInitializeEx один раз при импорте - в том потоке, который
# импортировал модуль; второй и последующие потоки апартамента не получают и
# падают с CO_E_NOTINITIALIZED (0x800401F0), поэтому инициализируем сами
COINIT_MULTITHREADED = 0x0
_S_FALSE = 1
_RPC_E_CHANGED_MODE = 0x80010106


def _com_init() -> bool:
    """Заводит MTA-апартамент в текущем потоке. True → нужен CoUninitialize."""
    try:
        ole32 = ctypes.windll.ole32
        hr = ole32.CoInitializeEx(None, COINIT_MULTITHREADED) & 0xFFFFFFFF
    except Exception:
        return False
    if hr == _RPC_E_CHANGED_MODE:
        return False  # Апартамент уже есть, но другой модели - не наш, не трогаем
    return hr in (0, _S_FALSE)


def _com_uninit(owned: bool) -> None:
    if owned:
        try:
            ctypes.windll.ole32.CoUninitialize()
        except Exception:
            pass


class SoundEvent:
    """Одно направленное звуковое событие."""

    __slots__ = ("angle", "intensity", "confidence", "fb_known", "t")

    def __init__(self, angle: float, intensity: float,
                 confidence: float, fb_known: bool, t: float) -> None:
        self.angle = angle            # Градусы: 0 = вперёд, + = вправо, ±180 = за спиной
        self.intensity = intensity    # 0..1, громкость превышения над фоном
        self.confidence = confidence  # 0..1, насколько звук направленный
        self.fb_known = fb_known      # Достоверна ли ось перед/зад
        self.t = t                    # time.time() события

    def age(self, now: float | None = None) -> float:
        return (time.time() if now is None else now) - self.t

    def __repr__(self) -> str:
        return (f"SoundEvent(angle={self.angle:+.0f}, int={self.intensity:.2f}, "
                f"conf={self.confidence:.2f}, fb={'yes' if self.fb_known else 'no'})")

def _band_energy(spec: np.ndarray, freq: np.ndarray, lo: float, hi: float) -> float:
    """Суммарная энергия спектра в полосе [lo, hi) Гц."""
    return float(spec[(freq >= lo) & (freq < hi)].sum())


def analyse_block(data: np.ndarray, names: list[str]) -> tuple[float, float, bool, float]:
    """
    Чистая функция (тестируется без звуковой карты).

    Вход: data (frames, nch) float, names - имена каналов.
    Выход: (angle_deg, confidence, fb_known, level_rms)

    Многоканал: сумма единичных векторов по углам каналов, взвешенная
    энергией. Стерео: L/R даёт азимут честно, перед/зад оценивается по
    спектральному наклону (HRTF глушит верх у звуков сзади).
    """
    if data.ndim == 1:
        data = data[:, None]

    rms = np.sqrt(np.mean(data.astype(np.float64) ** 2, axis=0))
    level = float(np.sqrt(np.mean(rms ** 2)))

    directional = [(n, r) for n, r in zip(names, rms)
                   if CHANNEL_ANGLES.get(n) is not None]
    if not directional or level <= 0.0:
        return 0.0, 0.0, False, level

    # ── Многоканал: истинный пеленг по дискретным каналам ──────────
    if len(directional) > 2:
        vx = vy = 0.0
        for name, r in directional:
            a = math.radians(CHANNEL_ANGLES[name])
            e = float(r) ** 2  # Энергия, не амплитуда
            vx += e * math.sin(a)
            vy += e * math.cos(a)
        total = sum(float(r) ** 2 for _, r in directional)
        mag = math.hypot(vx, vy)
        conf = mag / total if total > 0 else 0.0  # 1 = один канал, 0 = равномерно
        angle = math.degrees(math.atan2(vx, vy)) if mag > 0 else 0.0
        return angle, conf, True, level

    # ── Стерео: азимут по L/R, перед/зад по спектру ────────────────
    l, r = float(rms[0]), float(rms[1])
    denom = l + r
    pan = (r - l) / denom if denom > 0 else 0.0  # -1 = лево, +1 = право
    lr_conf = min(1.0, abs(pan) / 0.7)

    mono = data.mean(axis=1)
    win = mono * np.hanning(len(mono))
    spec = np.abs(np.fft.rfft(win))
    freq = np.fft.rfftfreq(len(win), 1.0 / SAMPLERATE)
    lo_e = _band_energy(spec, freq, TILT_LO_HZ, TILT_HI_HZ)
    hi_e = _band_energy(spec, freq, TILT_HI_HZ, TILT_HI2_HZ)
    tilt_db = 20.0 * math.log10(max(hi_e, 1e-12) / max(lo_e, 1e-12))

    # Глухой (мало верха) => трактуем как "сзади"
    behind = tilt_db < -TILT_MARGIN_DB
    fb_known = abs(tilt_db) > TILT_MARGIN_DB

    # pan => азимут на полукруге, затем зеркалим назад при глухом тембре
    front_angle = math.degrees(math.asin(max(-1.0, min(1.0, pan))))
    angle = (180.0 - front_angle) if behind and front_angle >= 0 else \
            (-180.0 - front_angle) if behind else front_angle

    conf = min(STEREO_CONFIDENCE, lr_conf)
    return angle, conf, fb_known, level

def _is_virtual(name: str) -> bool:
    low = name.lower()
    return any(h in low for h in VIRTUAL_HINTS)


class AudioCapture:
    """
    Фоновый сборщик направленных звуковых событий.

    Публичные поля (читать без блокировок):
      status        - строка для UI
      device_name   - выбранный endpoint
      channels      - сколько каналов реально снимаем
      mode          - "surround" | "stereo" | "off"
    """

    def __init__(self) -> None:
        self.status = "not started"
        self.device_name = ""
        self.channels = 0
        self.channel_names: list[str] = []
        self.mode = "off"
        self.level_db = -120.0

        self._events: deque[SoundEvent] = deque(maxlen=64)
        self._lock = threading.Lock()
        self._running = False
        self._thread: threading.Thread | None = None
        self._locked_device = False  # True после первого реального звука
        self._swept = False          # True после полного обхода кандидатов без звука
        self.preferred_device = ""   # "" = авто-выбор; иначе точное имя endpoint'а

    # ── Жизненный цикл ────────────────────────────────────────────
    def start(self) -> None:
        # Дожидаемся предыдущий поток: он блокируется в rec.record() и видит
        # флаг с задержкой, а на выходе выставляет mode="off". Без join он
        # затирал бы состояние только что поднятого потока
        prev = self._thread
        if prev is not None and prev.is_alive():
            self._running = False
            prev.join(timeout=1.0)

        self._running = True
        self._locked_device = False  # Перевыбрать endpoint: железо могло смениться
        self._swept = False
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        th, self._thread = self._thread, None
        if th is not None and th.is_alive():
            th.join(timeout=1.0)
        self.mode = "off"
        self.status = "stopped"

    # ── Чтение событий ────────────────────────────────────────────
    def recent(self, max_age: float) -> list[SoundEvent]:
        now = time.time()
        with self._lock:
            return [e for e in self._events if now - e.t <= max_age]

    # ── Выбор устройства ──────────────────────────────────────────
    @staticmethod
    def list_devices() -> list[tuple[str, int, bool]]:
        """[(имя, каналов, виртуальное?)] — для комбо-бокса в UI."""
        import soundcard as sc
        out = []
        for m in sc.all_microphones(include_loopback=True):
            if m.isloopback:
                out.append((m.name, m.channels, _is_virtual(m.name)))
        return out

    def _candidates(self, sc) -> list:
        """
        Физические endpoint'ы вперёд, виртуальные назад.

        Виртуальные surround-драйверы (Razer, Sonic, NVIDIA) рапортуют 8
        каналов, но их loopback отдаёт тишину — замерено. Поэтому число
        каналов вторично, «физичность» первична.

        Явный выбор пользователя (preferred_device) идёт первым и не
        ротируется по тишине: если человек указал устройство сам, мы не
        имеем права молча уехать на другое.
        """
        mics = [m for m in sc.all_microphones(include_loopback=True) if m.isloopback]
        mics.sort(key=lambda m: (_is_virtual(m.name), -m.channels))

        want = self.preferred_device
        if want:
            picked = [m for m in mics if m.name == want]
            if picked:
                return picked
        return mics

    # ── Основной цикл ─────────────────────────────────────────────
    def _loop(self) -> None:
        try:
            import soundcard as sc
        except Exception as exc:
            self.status = f"soundcard missing: {exc}"
            self.mode = "off"
            return

        # Без своего апартамента второй и последующие запуски падают
        # с CO_E_NOTINITIALIZED (см. комментарий у _com_init())
        com_owned = _com_init()
        try:
            idx = 0
            while self._running:
                try:
                    cands = self._candidates(sc)
                    if not cands:
                        self.status = "no loopback endpoint"
                        time.sleep(2.0)
                        continue
                    mic = cands[idx % len(cands)]
                    rotated = self._session(mic)
                    if rotated and not self._locked_device:
                        # Тишина неотличима от "в системе просто ничего не играет",
                        # поэтому обходим кандидатов ОДИН раз, а затем "паркуемся"
                        # на первом (физическом) и ждём звук там. Иначе покой в
                        # системе уводил нас на мёртвый виртуальный endpoint.
                        idx += 1
                        if idx >= len(cands):
                            idx = 0
                            self._swept = True
                except Exception as exc:
                    self.status = f"{type(exc).__name__}: {exc}"
                    time.sleep(1.5)
        finally:
            _com_uninit(com_owned)

    def _session(self, mic) -> bool:
        """
        Одна сессия записи. Возвращает True, если стоит сменить устройство
        (устройство отдаёт bit-exact тишину дольше SILENCE_SWITCH_S).
        """
        nch = mic.channels
        names = LAYOUTS.get(nch, [f"ch{i}" for i in range(nch)])
        pinned = bool(self.preferred_device)

        self.device_name = mic.name
        self.channels = nch
        self.channel_names = names
        self.mode = "surround" if nch > 2 else "stereo"
        self.status = f"listening ({nch}ch)"

        baseline: deque[float] = deque(maxlen=BASELINE_BLOCKS)
        last_event = 0.0
        silent_since = time.time()

        with mic.recorder(samplerate=SAMPLERATE, channels=nch, blocksize=BLOCK) as rec:
            while self._running:
                data = rec.record(numframes=BLOCK)
                if data.ndim == 1:
                    data = data[:, None]
                data = data.astype(np.float64)

                now = time.time()

                # Bit-exact нули = либо тишина в системе, либо мёртвый endpoint
                # Различаем по времени: живой endpoint рано или поздно даёт звук
                silent_block = not np.any(data)
                if silent_block:
                    if (not self._locked_device and not pinned and not self._swept
                            and now - silent_since > SILENCE_SWITCH_S):
                        self.status = f"silent, trying next ({nch}ch)"
                        return True
                    # Приколоченное руками или уже обойдённое устройство не меняем:
                    # сидим и ждём звук, честно показывая, что его нет
                    if not self._locked_device and now - silent_since > SILENCE_SWITCH_S:
                        self.status = (f"{nch}ch selected, but silent" if pinned
                                       else f"{nch}ch, waiting for sound")
                else:
                    silent_since = now
                    self._locked_device = True
                    self.status = f"listening ({nch}ch)"

                # Энергия в полосе шагов - для onset-детекта.
                # ВАЖНО: тишина тоже идёт в baseline, иначе фон состоит только из
                # громких блоков и превышение над ним никогда не наступает.
                mono = data.mean(axis=1)
                spec = np.abs(np.fft.rfft(mono * np.hanning(len(mono))))
                freq = np.fft.rfftfreq(len(mono), 1.0 / SAMPLERATE)
                band = _band_energy(spec, freq, BAND_LO_HZ, BAND_HI_HZ)
                band_rms = band / max(len(mono), 1)
                band_db = 20.0 * math.log10(max(band_rms, 1e-9))
                self.level_db = band_db

                # Фон копим всегда; пока он не набран - только учимся, не стреляем.
                ready = len(baseline) >= BASELINE_MIN
                base = float(np.median(baseline)) if ready else FLOOR_DB
                baseline.append(band_db)

                if silent_block or not ready:
                    continue
                if band_db < FLOOR_DB or band_db < base + RISE_DB:
                    continue
                if now - last_event < COOLDOWN_S:
                    continue

                angle, conf, fb_known, _ = analyse_block(data, names)
                if conf < MIN_CONFIDENCE:
                    continue  # Всенаправленно: свой выстрел, музыка, эмбиент

                intensity = max(0.0, min(1.0, (band_db - base) / 30.0))
                last_event = now
                with self._lock:
                    self._events.append(
                        SoundEvent(angle, intensity, conf, fb_known, now))

        return False


# Экземпляр класса AudioCapture для импорта в скрипт/оверлей
audio_capture = AudioCapture()

