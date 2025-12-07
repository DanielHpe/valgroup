from src.services.excel_service import ExcelService
from src.services.file_service import FileService
from src.services.system_service import SystemService
from src.utils.webdriver import WebDriver
from src.views.email_view import EmailView
from src.views.results_view import ResultsView


class JobController:
    def execute(self) -> None:
        file_service = FileService()

        file_service.clear_folder(file_service.get_download_folder())

        driver = WebDriver(file_service.get_download_folder(), False).open_browser()

        sistema_service = SystemService(driver)

        is_login_successful = sistema_service.login()

        if not is_login_successful["status"]:
            driver.quit()
            raise Exception(is_login_successful["message"])

        is_download_report_successful = sistema_service.download_report(file_service)

        if not is_download_report_successful["status"]:
            sistema_service.logout()
            driver.quit()
            raise Exception(is_download_report_successful["message"])

        abs_downloaded_file = "\\".join(
            [
                file_service.get_download_folder(),
                file_service.get_downloaded_files()[0]
            ]
        )
        excel_service = ExcelService(abs_downloaded_file)

        is_excel_data_successful = excel_service.load_employees_from_excel()

        if not is_excel_data_successful["status"]:
            sistema_service.logout()
            driver.quit()
            raise Exception(is_excel_data_successful["message"])

        employees = is_excel_data_successful["data"]

        is_employees_registred = sistema_service.signup_employees(employees)

        if "data" not in is_employees_registred:
            sistema_service.logout()
            driver.quit()
            raise Exception(is_employees_registred["message"])

        list_of_employees = is_employees_registred["data"]

        results_view = ResultsView(len(employees), list_of_employees)
        results_view.report_results()

        sistema_service.logout()
        driver.quit()

        email_view = EmailView()
        email_body = email_view.build_email_body(list_of_employees)
        email_view.set_email_body(email_body)
        email_view.send_mail()

        return
