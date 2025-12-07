import sys
import traceback

from src.controllers.job_controller import JobController
from src.services.report_service import ReportService
from src.utils.constants import LOG_ERROR_LEVEL, LOG_INFO_LEVEL
from src.utils.enviroment import Environment


def main() -> int:
    try:
        ReportService.send_report("Iniciando execução da aplicação...", LOG_INFO_LEVEL)
        job_controller = JobController()
        job_controller.execute()
        ReportService.send_report("Finalizando execução da aplicação...", LOG_INFO_LEVEL)
        return 0
    except Exception as e:
        error_details = traceback.format_exc()
        ReportService.send_report(f"Erro ao executar a aplicação: {e}\n{error_details}", LOG_ERROR_LEVEL)
        return 1


if __name__ == "__main__":
    env = Environment()
    env.setup_env()
    exit_code = main()
    sys.exit(exit_code)
