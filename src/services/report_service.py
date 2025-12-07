from src.services.log_service import LogService


class ReportService:
    _log_service = LogService(name="ValGroup", logfile="app.log")

    @staticmethod
    def send_report(message: str, log_level: str = "INFO") -> None:
        if log_level == "INFO":
            ReportService._log_service.info(message)
        elif log_level == "DEBUG":
            ReportService._log_service.debug(message)
        elif log_level == "WARNING":
            ReportService._log_service.warning(message)
        elif log_level == "ERROR":
            ReportService._log_service.error(message)
