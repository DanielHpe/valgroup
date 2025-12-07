from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager


class WebDriver:
    def __init__(self, download_folder: str, no_window_mode: bool = True, parameters: list[str] = None):
        if parameters is None:
            parameters = []
        self.options = Options()
        self.options.add_experimental_option("prefs", {
            "download.default_directory": download_folder,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        if no_window_mode:
            self.options.add_argument("--headless=new")
        self.options.add_argument("--allow-running-insecure-content")
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--log-level=3")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-dev-shm-usage")
        if len(parameters) > 0:
            for parameter in parameters:
                self.options.add_argument(parameter)

    def open_browser(self) -> WebDriver | str:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=self.options
        )
        return driver
