import os
import pathlib
import shutil

from src.services.report_service import ReportService
from src.utils.constants import LOG_INFO_LEVEL, LOG_WARNING_LEVEL


class FileService:
    def __init__(self):
        self.project_folder = pathlib.Path(__file__).resolve().parent.parent
        self.download_folder = os.path.join(self.project_folder, "files", "downloads")

    def file_exists(self, filename: str) -> bool:
        return os.path.isfile(filename)

    def get_download_folder(self) -> str:
        os.makedirs(self.download_folder, exist_ok=True)
        return self.download_folder

    def clear_folder(self, folder_path: str):
        ReportService.send_report(f"Limpando diretorio de downloads {self.download_folder}", LOG_INFO_LEVEL)
        if not os.path.exists(folder_path):
            return False  # pasta não existe

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                ReportService.send_report(f"Erro ao deletar! {e}", LOG_WARNING_LEVEL)
                return False

        ReportService.send_report("Limpeza do diretorio realizada com sucesso!", LOG_INFO_LEVEL)
        return True

    def get_downloaded_files(self):
        if not os.path.exists(self.download_folder):
            return []

        return [
            f for f in os.listdir(self.download_folder)
            if os.path.isfile(os.path.join(self.download_folder, f))
        ]
