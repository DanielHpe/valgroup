import pandas as pd
from pydantic import ValidationError

from src.models.employee import Employee
from src.services.report_service import ReportService
from src.utils.constants import (
    ERROR_DATA_EXCEL,
    LOG_INFO_LEVEL,
    LOG_WARNING_LEVEL,
    NO_EXCEL_DATA,
    SUCCESS_GET_EXCEL_DATA,
)
from src.utils.response import Response


class ExcelService:
    def __init__(self, excel_file: str) -> None:
        self.excel_file = excel_file

    def load_employees_from_excel(self) -> list[Employee]:
        ReportService.send_report("Extraindo dados de funcionários do Excel...", LOG_INFO_LEVEL)
        df = pd.read_excel(self.excel_file)

        df = df.where(pd.notnull(df), None)

        employees: list[Employee] = []

        for _, row in df.iterrows():
            try:
                employee = Employee(**row.to_dict())
                employees.append(employee)
            except ValidationError:
                employees.append(Response.handle_response(False, ERROR_DATA_EXCEL))

        if employees == []:
            ReportService.send_report(NO_EXCEL_DATA, LOG_WARNING_LEVEL)
            return Response.handle_response(False, NO_EXCEL_DATA)

        ReportService.send_report(SUCCESS_GET_EXCEL_DATA, LOG_INFO_LEVEL)
        return Response.handle_response(True, SUCCESS_GET_EXCEL_DATA, employees)
