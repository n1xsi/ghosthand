"""
Системный монитор GhostHand.
Обновляет CPU%, GPU%, Ping в фоновом потоке.
"""
import socket
import threading
import time
import psutil
import GPUtil


class SysMonitor:
    """Фоновый сборщик системных метрик."""

    def __init__(self):
        self.cpu_percent: float = 0.0
        self.gpu_percent: float = 0.0
        self.ping_ms:     int = 0

        self._running = False

    def start(self) -> None:
        self._running = True
        threading.Thread(target=self._loop, daemon=True).start()

    # ── Основной цикл ─────────────────────────────────────────────
    def _loop(self) -> None:
        # Первый вызов — инициализация baseline
        psutil.cpu_percent(interval=1)

        ping_tick = 0
        while self._running:
            # CPU
            self.cpu_percent = psutil.cpu_percent(interval=None)

            # GPU
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    self.gpu_percent = gpus[0].load * 100.0
            except Exception:
                pass

            # Ping
            ping_tick += 1
            if ping_tick >= 5:  # Обновляется раз в 5 сек
                ping_tick = 0
                self._update_ping()

            time.sleep(1.0)

    def _update_ping(self) -> None:
        """TCP ping к 8.8.8.8:53 (Google DNS)."""
        try:
            start = time.perf_counter()
            with socket.create_connection(("8.8.8.8", 53), timeout=2):
                pass
            self.ping_ms = int((time.perf_counter() - start) * 1000)
        except Exception:
            self.ping_ms = 0


# Экземпляр класса SysMonitor для импорта в меню
sysmon = SysMonitor()
