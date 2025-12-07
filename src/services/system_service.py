import os
import time
import traceback
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from src.models.employee import Employee
from src.services.file_service import FileService
from src.services.report_service import ReportService
from src.utils.constants import (
    CONT_TENTATIVAS,
    DOWNLOAD_REPORT_ERROR,
    DOWNLOAD_REPORT_SUCCESS,
    ERROR_LIMIT_ATTEMPTS_SIGNUP_EMPLOYEE,
    ERROR_PAGE_MESSAGE,
    ERROR_SIGNUP_EMPLOYEE,
    ERROR_SIGNUP_PAGE_ACCESS,
    LOG_ERROR_LEVEL,
    LOG_INFO_LEVEL,
    LOG_WARNING_LEVEL,
    LOGIN_ERROR,
    LOGIN_SUCCESS,
    SUCCESS_SIGNUP_EMPLOYEE,
    SUCCESS_SIGNUP_PAGE_ACCESS,
)
from src.utils.response import Response
from src.utils.selenium import Selenium


class SystemService:
    def __init__(self, driver: WebDriver) -> None:
        self.access_url = os.environ["ACCESS_URL"]
        self.access_user = os.environ["ACCESS_USER"]
        self.access_password = os.environ["ACCESS_PASSWORD"]
        self.driver = driver

    def login(self) -> dict:
        """
            Efetua o login no sistema disponibilizado
        """
        for cont_tentativas in range(CONT_TENTATIVAS):
            try:
                ReportService.send_report(f"Tentativa {cont_tentativas + 1} de logar no sistema", LOG_INFO_LEVEL)
                ReportService.send_report(f"Acessando o ambiente {self.access_url}", LOG_INFO_LEVEL)
                Selenium.access_url(self.driver, self.access_url)
                ReportService.send_report("Preenchendo o usuario", LOG_INFO_LEVEL)
                Selenium.send_keys(
                    Selenium.wait_element_exists(
                        driver=self.driver,
                        element_locator="username",
                        element_type="ID",
                        max_time=15
                ), self.access_user)
                ReportService.send_report("Preenchendo a senha", LOG_INFO_LEVEL)
                Selenium.send_keys(
                    Selenium.wait_element_exists(
                        driver=self.driver,
                        element_locator="password",
                        element_type="ID",
                        max_time=15
                ), self.access_password)
                ReportService.send_report("Clicando em entrar", LOG_INFO_LEVEL)
                Selenium.click_element(
                    self.driver,
                    Selenium.wait_element_exists(
                        driver=self.driver,
                        element_locator="loginBtn",
                        element_type="ID",
                        max_time=15
                    )
                )
                ReportService.send_report("Validando se login foi efetuado com sucesso...", LOG_INFO_LEVEL)
                is_login_successful = Selenium.wait_element_exists(
                        driver=self.driver,
                        element_locator="/html/body/div/div/div[1]/i",
                        element_type="XPATH",
                        max_time=60
                    )
                if is_login_successful is None:
                    ReportService.send_report(LOGIN_ERROR, LOG_WARNING_LEVEL)
                    if cont_tentativas == CONT_TENTATIVAS - 1:
                        return Response.handle_response(False, f"{LOGIN_ERROR} - Validar credenciais de acesso!.")
                    ReportService.send_report("Tentando novamente...", LOG_WARNING_LEVEL)
                    continue

                ReportService.send_report(LOGIN_SUCCESS, LOG_INFO_LEVEL)
                return Response.handle_response(True, LOGIN_SUCCESS)
            except Exception as e:
                error_details = traceback.format_exc()
                ReportService.send_report(f"{LOGIN_ERROR} - {e}\n{error_details}", LOG_ERROR_LEVEL)
                if cont_tentativas == CONT_TENTATIVAS - 1:
                    return Response.handle_response(False, f"{LOGIN_ERROR} - {e}\n{error_details}")
                ReportService.send_report("Tentando novamente...", LOG_INFO_LEVEL)
                time.sleep(5)

    def download_report(self, file_: FileService) -> dict:
        """
            Efetua o Download da Planilha de funcionários
        """
        for cont_tentativas in range(CONT_TENTATIVAS):
            try:
                ReportService.send_report(f"Tentativa {cont_tentativas + 1} de baixar o relatorio de funcionarios", LOG_INFO_LEVEL)
                ReportService.send_report("Acessando o Menu de Download...", LOG_INFO_LEVEL)
                ReportService.send_report("Baixando relatório...", LOG_INFO_LEVEL)
                Selenium.click_element(
                    self.driver,
                    Selenium.wait_element_exists(
                        driver=self.driver,
                        element_locator="/html/body/div/div/div[4]/div[1]/div/div/a",
                        element_type="XPATH",
                        max_time=15
                    )
                )

                # Validando mensagem de erro na tela
                if Selenium.find_element(self.driver, "lead", "CLASS") is None:
                    # Caso nenhuma mensagem de erro, Download realizado com sucesso!
                    time.sleep(10)
                    if any(Path(file_.get_download_folder()).iterdir()):
                        abs_downloaded_file = "\\".join(
                            [
                                file_.get_download_folder(),
                                file_.get_downloaded_files()[0]
                            ]
                        )
                        if file_.file_exists(abs_downloaded_file):
                            ReportService.send_report(DOWNLOAD_REPORT_SUCCESS, LOG_INFO_LEVEL)
                            return Response.handle_response(True, DOWNLOAD_REPORT_SUCCESS)
                    else:
                        ReportService.send_report(DOWNLOAD_REPORT_ERROR, LOG_WARNING_LEVEL)
                        if cont_tentativas == CONT_TENTATIVAS - 1:
                            return Response.handle_response(False, DOWNLOAD_REPORT_ERROR)
                        continue

                # Caso mensagem de erro, bot tenta baixar o relatório até 10 tentativas
                cont_tentativas_erro_site = 0
                error_message_page = "OK"
                while Selenium.find_element(self.driver, "lead", "CLASS") and cont_tentativas_erro_site < 10:
                    error_message_page = Selenium.find_element(self.driver, "lead", "CLASS").text.strip()
                    if error_message_page == ERROR_PAGE_MESSAGE:
                        cont_tentativas_erro_site = cont_tentativas_erro_site + 1
                        ReportService.send_report(
                            f"Tentativa {cont_tentativas_erro_site} - Erro ao acessar relatório. Tentando novamente em 15 segundos...",
                            LOG_WARNING_LEVEL
                        )
                        time.sleep(5)
                        self.driver.refresh()
                        time.sleep(10)
                        if any(Path(file_.get_download_folder()).iterdir()):
                            abs_downloaded_file = "\\".join(
                                [
                                    file_.get_download_folder(),
                                    file_.get_downloaded_files()[0]
                                ]
                            )
                            if file_.file_exists(abs_downloaded_file):
                                error_message_page = "OK"
                                break

                # Caso relatório não baixado depois de 10 tentativas, retorna erro
                if error_message_page != "OK":
                    self.driver.back()
                    ReportService.send_report(DOWNLOAD_REPORT_ERROR, LOG_WARNING_LEVEL)
                    if cont_tentativas == CONT_TENTATIVAS:
                        return Response.handle_response(False, DOWNLOAD_REPORT_ERROR)
                    continue

                # Caso sucesso! Retorna para a página anterior (Download realizado com sucesso!)
                self.driver.back()
                time.sleep(5)
                ReportService.send_report(DOWNLOAD_REPORT_SUCCESS, LOG_INFO_LEVEL)
                return Response.handle_response(True, DOWNLOAD_REPORT_SUCCESS)
            except Exception as e:
                file_.clear_folder(file_.get_download_folder())
                error_details = traceback.format_exc()
                ReportService.send_report(f"{DOWNLOAD_REPORT_ERROR}: {e}\n{error_details}", LOG_ERROR_LEVEL)
                if cont_tentativas == CONT_TENTATIVAS - 1:
                    return Response.handle_response(False, f"{DOWNLOAD_REPORT_ERROR} {e}\n{error_details}")
                ReportService.send_report("Tentando novamente...", LOG_INFO_LEVEL)
                time.sleep(5)

    def __navigate_to_signup_page(self) -> bool:
        for cont_tentativas in range(CONT_TENTATIVAS):
            try:
                # Acessando pagina de cadastro
                ReportService.send_report(f"Tentativa {cont_tentativas + 1} de navegar a pagina de cadastro", LOG_INFO_LEVEL)
                ReportService.send_report("Navegando ate a pagina de cadastro", LOG_INFO_LEVEL)
                Selenium.click_element(
                    self.driver,
                    Selenium.wait_element_exists(
                        driver=self.driver,
                        element_locator="btn-warning",
                        element_type="CLASS_NAME",
                        max_time=15
                    )
                )
                is_sigunp_window_exists = Selenium.wait_element_exists(
                    driver=self.driver,
                    element_locator="h1",
                    element_type="TAG_NAME",
                    max_time=30
                )

                # Validando se pagina de cadastro existe na tela
                if is_sigunp_window_exists is None:
                    ReportService.send_report(ERROR_SIGNUP_PAGE_ACCESS, LOG_WARNING_LEVEL)
                    if cont_tentativas == CONT_TENTATIVAS - 1:
                        return False
                    ReportService.send_report("Tentando novamente...", LOG_WARNING_LEVEL)
                    time.sleep(5)
                    continue

                # Validando se texto recuperado contem a informacao cadastro
                if "Cadastro" not in is_sigunp_window_exists.text:
                    ReportService.send_report(ERROR_SIGNUP_PAGE_ACCESS, LOG_WARNING_LEVEL)
                    if cont_tentativas == CONT_TENTATIVAS - 1:
                        return False
                    ReportService.send_report("Tentando novamente...", LOG_WARNING_LEVEL)
                    time.sleep(5)
                    continue

                ReportService.send_report(SUCCESS_SIGNUP_PAGE_ACCESS, LOG_INFO_LEVEL)
                return True
            except Exception as e:
                input("Erro aqui")
                self.driver.refresh()
                error_details = traceback.format_exc()
                ReportService.send_report(f"{ERROR_SIGNUP_PAGE_ACCESS} - {e}\n{error_details}", LOG_ERROR_LEVEL)
                if cont_tentativas == CONT_TENTATIVAS - 1:
                    return False
                ReportService.send_report("Tentando novamente...", LOG_INFO_LEVEL)
                time.sleep(5)

    def signup_employees(self, employees: list[Employee]) -> dict:
        """
            Efetua o cadastro dos funcionários no sistema
        """
        sigunp_page_access_successful = self.__navigate_to_signup_page()
        list_of_employees_registered_and_not_registered = []

        if not sigunp_page_access_successful:
            return Response.handle_response(False, ERROR_SIGNUP_PAGE_ACCESS)

        ReportService.send_report(f"Realizando o cadastro de {len(employees)} funcionarios.", LOG_INFO_LEVEL)

        for cont_employees, employee in enumerate(employees):
            for cont_tentativas in range(CONT_TENTATIVAS):
                try:
                    # Clicando no botao de cadastro
                    ReportService.send_report(
                        f"Tentativa {cont_tentativas + 1} de cadastrar funcionario numero {cont_employees + 1}",
                        LOG_INFO_LEVEL
                    )
                    ReportService.send_report(
                        f"Realizando o cadastro do funcionario numero {cont_employees + 1} da planilha...",
                        LOG_INFO_LEVEL
                    )
                    # Preenchendo informaçoes do funcionario
                    Selenium.switch_to_frame(
                        self.driver,
                        Selenium.wait_element_exists(
                            driver=self.driver,
                            element_locator="registerIframe",
                            element_type="ID",
                            max_time=15
                        )
                    )
                    ReportService.send_report("Preenchendo email...", LOG_INFO_LEVEL)
                    Selenium.send_keys(
                        Selenium.wait_element_exists(
                            driver=self.driver,
                            element_locator="//label[contains(normalize-space(.), 'Email')]/following::input[1]",
                            element_type="XPATH",
                            max_time=15,
                    ), employee.email)
                    ReportService.send_report("Preenchendo endereço...", LOG_INFO_LEVEL)
                    Selenium.send_keys(
                        Selenium.wait_element_exists(
                            driver=self.driver,
                            element_locator="//label[contains(normalize-space(.), 'Endereço')]/following::textarea[1]",
                            element_type="XPATH",
                            max_time=15,
                    ), employee.address)
                    ReportService.send_report("Preenchendo cargo...", LOG_INFO_LEVEL)
                    Selenium.send_keys(
                        Selenium.wait_element_exists(
                            driver=self.driver,
                            element_locator="//label[contains(normalize-space(.), 'Cargo')]/following::input[1]",
                            element_type="XPATH",
                            max_time=15,
                    ), employee.job)
                    ReportService.send_report("Preenchendo sobrenome...", LOG_INFO_LEVEL)
                    Selenium.send_keys(
                        Selenium.wait_element_exists(
                            driver=self.driver,
                            element_locator="//label[contains(normalize-space(.), 'Sobrenome')]/following::input[1]",
                            element_type="XPATH",
                            max_time=15,
                    ), employee.surname)
                    ReportService.send_report("Preenchendo telefone...", LOG_INFO_LEVEL)
                    Selenium.send_keys(
                        Selenium.wait_element_exists(
                            driver=self.driver,
                            element_locator="//label[contains(normalize-space(.), 'Telefone')]/following::input[1]",
                            element_type="XPATH",
                            max_time=15,
                    ), employee.phone)
                    ReportService.send_report("Preenchendo empresa...", LOG_INFO_LEVEL)
                    Selenium.send_keys(
                        Selenium.wait_element_exists(
                            driver=self.driver,
                            element_locator="//label[contains(normalize-space(.), 'Empresa')]/following::input[1]",
                            element_type="XPATH",
                            max_time=15,
                    ), employee.company)
                    ReportService.send_report("Preenchendo nome...", LOG_INFO_LEVEL)
                    Selenium.send_keys(
                        Selenium.wait_element_exists(
                            driver=self.driver,
                            element_locator="//label[contains(normalize-space(.), 'Nome')]/following::input[1]",
                            element_type="XPATH",
                            max_time=15,
                    ), employee.name)
                    ReportService.send_report("Cadastrando...", LOG_INFO_LEVEL)
                    Selenium.click_element(
                        self.driver,
                        Selenium.wait_element_exists(
                            driver=self.driver,
                            element_locator="button[type='submit']",
                            element_type="CSS_SELECTOR",
                            max_time=15
                        )
                    )
                    is_sigunp_successful = Selenium.wait_element_exists(
                        driver=self.driver,
                        element_locator="alert-success",
                        element_type="CLASS_NAME",
                        max_time=30
                    )

                    if is_sigunp_successful is None:
                        self.driver.refresh()
                        ReportService.send_report(f"{ERROR_SIGNUP_EMPLOYEE} Instabilidade temporaria do sistema!!", LOG_WARNING_LEVEL)
                        if cont_tentativas == CONT_TENTATIVAS - 1:
                            list_of_employees_registered_and_not_registered.append(
                                Response.handle_response(
                                    False,
                                    ERROR_LIMIT_ATTEMPTS_SIGNUP_EMPLOYEE,
                                    employee
                                    )
                                )
                            ReportService.send_report(ERROR_LIMIT_ATTEMPTS_SIGNUP_EMPLOYEE, LOG_WARNING_LEVEL)
                            break
                        ReportService.send_report("Tentando novamente...", LOG_WARNING_LEVEL)
                        time.sleep(5)
                        continue

                    # Validando se texto recuperado contem a informacao cadastro
                    if "Funcionário cadastrado com sucesso!" not in is_sigunp_successful.text:
                        self.driver.refresh()
                        ReportService.send_report(ERROR_SIGNUP_EMPLOYEE, LOG_WARNING_LEVEL)
                        if cont_tentativas == CONT_TENTATIVAS - 1:
                            list_of_employees_registered_and_not_registered.append(
                                Response.handle_response(
                                    False,
                                    ERROR_LIMIT_ATTEMPTS_SIGNUP_EMPLOYEE,
                                    employee
                                )
                            )
                            ReportService.send_report(ERROR_LIMIT_ATTEMPTS_SIGNUP_EMPLOYEE, LOG_WARNING_LEVEL)
                            break
                        ReportService.send_report("Tentando novamente...", LOG_WARNING_LEVEL)
                        time.sleep(5)
                        continue

                    list_of_employees_registered_and_not_registered.append(
                        Response.handle_response(
                            True,
                            SUCCESS_SIGNUP_EMPLOYEE,
                            employee
                        )
                    )
                    ReportService.send_report(SUCCESS_SIGNUP_EMPLOYEE, LOG_INFO_LEVEL)
                    self.driver.refresh()
                    break
                except Exception as e:
                    self.driver.refresh()
                    error_details = traceback.format_exc()
                    ReportService.send_report(f"Erro ao cadastrar funcionario: {e}\n{error_details}", LOG_ERROR_LEVEL)
                    if cont_tentativas == CONT_TENTATIVAS - 1:
                        ReportService.send_report("Não foi possivel cadastrar funcionario!!", LOG_WARNING_LEVEL)
                        continue
                    ReportService.send_report("Tentando novamente...", LOG_INFO_LEVEL)
                    time.sleep(5)

        return Response.handle_response(True, "Funcionarios, processados", list_of_employees_registered_and_not_registered)

    def logout(self) -> dict:
        for _ in range(CONT_TENTATIVAS):
            try:
                ReportService.send_report("Deslogando do sistema...", LOG_INFO_LEVEL)
                Selenium.click_element(
                    self.driver,
                    Selenium.wait_element_exists(
                        driver=self.driver,
                        element_locator="btn-outline-danger",
                        element_type="CLASS_NAME",
                        max_time=15
                    )
                )
                ReportService.send_report("Usuario deslogado com sucesso", LOG_INFO_LEVEL)
                time.sleep(5)
                return True
            except Exception:
                self.driver.refresh()
                time.sleep(5)
                return False
