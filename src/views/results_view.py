from src.services.report_service import ReportService
from src.utils.constants import LOG_INFO_LEVEL


class ResultsView:
    def __init__(self, total_of_users_executed, list_of_employees) -> None:
        self.total_of_users_executed = total_of_users_executed
        self.list_of_employees = list_of_employees

    def get_total_of_employees_registered(self) -> int:
        return sum(1 for item in self.list_of_employees if item.get("status"))

    def get_total_of_employees_not_registered(self) -> int:
        return sum(1 for item in self.list_of_employees if not item.get("status"))

    def report_results(self) -> None:
        ReportService.send_report(
            "#### PRINTANDO RESULTADOS FINAIS ####",
            LOG_INFO_LEVEL
        )
        ReportService.send_report(
            f"TOTAL DE FUNCIONARIOS PROCESSADOS DO RELATORIO: {self.total_of_users_executed}",
            LOG_INFO_LEVEL
        )
        ReportService.send_report(
            f"TOTAL DE FUNCIONARIOS CADASTRADOS COM SUCESSO: {self.get_total_of_employees_registered()}",
            LOG_INFO_LEVEL
        )
        ReportService.send_report(
            f"TOTAL DE FUNCIONARIOS NAO CADASTRADOS (HOUVE ERRO): {self.get_total_of_employees_not_registered()}",
            LOG_INFO_LEVEL
        )
