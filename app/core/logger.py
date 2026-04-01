import os
from datetime import datetime


class Logger:
    def __init__(self, logFileName: str) -> None:
        self.logFileName = logFileName
        self.logFilePath = ""

        if self.logFileName:
            self.create_log_file()

    def create_log_file(self) -> None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        log_dir = os.path.join(base_dir, "data", "logs")
        self.logFilePath = os.path.join(log_dir, self.logFileName)

        os.makedirs(log_dir, exist_ok=True)

        if not os.path.exists(self.logFilePath):
            with open(self.logFilePath, "w", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write("SAVE-RESTRICTED-CONTENT-BOT-LOGS\n")
                f.write("=" * 60 + "\n\n")

    def _write(self, level: str, msg: str, module: str = "Core") -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = f"[{timestamp}] [{level}] [{module}] {msg}"

        print(log)

        if self.logFilePath:
            with open(self.logFilePath, "a", encoding="utf-8") as f:
                f.write(log + "\n")

    def info(self, msg: str, module: str = "Core") -> None:
        self._write("INFO", msg, module)

    def warning(self, msg: str, module: str = "Core") -> None:
        self._write("WARNING", msg, module)

    def error(self, msg: str, module: str = "Core") -> None:
        self._write("ERROR", msg, module)


logFileName = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log = Logger(logFileName)
