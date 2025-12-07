import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.services.report_service import ReportService
from src.utils.constants import (
    EMAIL_QUESTION_1,
    EMAIL_QUESTION_2,
    EMAIL_QUESTION_3,
    EMAIL_QUESTION_4,
    EMAIL_SUBJECT,
    LOG_INFO_LEVEL,
    LOG_WARNING_LEVEL,
)


class EmailView:
    def __init__(
            self,
            email_body: str = ""
        ):
        self.email_body = email_body

    def set_email_body(self, email_body):
        self.email_body = email_body

    def build_email_body(self, list_of_employees: list[dict]) -> str:
        lines = ["Lista de funcionarios processados\n"]

        for item in list_of_employees:
            employee = item["data"]
            full_name = f"{employee.name} {employee.surname}"

            if item.get("status"):
                status_line = "Cadastrado com sucesso!"
            else:
                error_message = item.get("message")
                status_line = "Falha no cadastro!"
                status_line += f"\nMotivo: {error_message}"

            lines.append(f"Funcionario: {full_name}")
            lines.append(f"Status: {status_line}\n")

        return "\n".join(lines)

    def __validate_to_send_email__(self):
        wish_to_send_email = input(EMAIL_QUESTION_1)
        if (wish_to_send_email != "s"):
            return False

        self.sender_email = input(EMAIL_QUESTION_2)
        self.app_password = input(EMAIL_QUESTION_3)
        self.receiver_email = input(EMAIL_QUESTION_4)

        return True

    def send_mail(self):
        try:
            if not self.__validate_to_send_email__():
                ReportService.send_report(
                    "Usuario nao deseja enviar os resultados por email!",
                    LOG_INFO_LEVEL
                )
                return False

            ReportService.send_report("Enviando email com os resultados", LOG_INFO_LEVEL)
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = self.receiver_email
            message["Subject"] = EMAIL_SUBJECT
            message.attach(MIMEText(self.email_body, "plain"))

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.sender_email, self.app_password)
                server.sendmail(self.sender_email, self.receiver_email, message.as_string())

            ReportService.send_report("Email enviado com sucesso!!", LOG_INFO_LEVEL)
            return True
        except Exception as e:
            error_details = traceback.format_exc()
            ReportService.send_report(f"Erro ao enviar email - {e}\n{error_details}", LOG_WARNING_LEVEL)
            return False
