import threading


class ScriptBase:
    """
    Базовый класс для всех скриптов GhostHand.

    Даёт:
      - self.running / self.enabled
      - start() → запускает _loop() в daemon-потоке

    Скрипты с нестандартным запуском (Bhop, SnapTap) переопределяют start().
    """

    def __init__(self) -> None:
        self.running = False
        self.enabled = False

    def start(self) -> None:
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self) -> None:
        raise NotImplementedError(f"{type(self).__name__} must implement _loop()")
