import datetime


class LogService:
    RESET = "\033[0m"
    COLORS = {
        "INFO": "\033[34m",    # Blue
        "DEBUG": "\033[36m",   # Cyan
        "WARNING": "\033[33m", # Yellow
        "ERROR": "\033[31m",   # Red
    }

    def __init__(self, name: str = "APP", logfile: str = None):
        self.name = name
        self.logfile = logfile

        if logfile:
            self._file = open(logfile, "a", encoding="utf-8")
        else:
            self._file = None

    def __define_timestamp__(self) -> datetime:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __write__(self, level: str, message: str) -> None:
        color = self.COLORS.get(level, "")
        timestamp = self.__define_timestamp__()
        formatted = f"[{timestamp}] [{self.name}] [{level}] {message}"

        print(f"{color}{formatted}{self.RESET}")

        if self._file:
            self._file.write(formatted + "\n")
            self._file.flush()

    def info(self, message: str) -> None:
        self.__write__("INFO", message)

    def debug(self, message: str) -> None:
        self.__write__("DEBUG", message)

    def warning(self, message: str) -> None:
        self.__write__("WARNING", message)

    def error(self, message: str):
        self.__write__("ERROR", message)

    def __del__(self) -> None:
        if self._file:
            self._file.close()
