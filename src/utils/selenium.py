from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    JavascriptException,
    NoSuchElementException,
    NoSuchFrameException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class Selenium:
    @staticmethod
    def access_url(driver: WebDriver, url: str) -> None:
        return driver.get(url)

    @staticmethod
    def wait_element_exists(
        driver: WebDriver,
        element_locator: str,
        element_type: str = "XPATH",
        max_time: int = 60
    ) -> WebElement:
        try:
            return WebDriverWait(driver, max_time).until(
                ec.presence_of_element_located(
                    (By().__getattribute__(element_type.upper()), element_locator)
                )
            )
        except TimeoutException:
            return None
        except AttributeError as ae:
            raise Exception("Tipo de elemento invalido") from ae

    @staticmethod
    def send_keys(element: WebElement, keystroke: str) -> None:
        if keystroke == "enter":
            keystroke = Keys.ENTER
        if keystroke == "home":
            keystroke = Keys.HOME
        try:
            actions = ActionChains(element)
            actions = actions.send_keys(keystroke)
            actions.perform()
        except (AttributeError, NoSuchElementException):
            element.send_keys(keystroke)

    @staticmethod
    def click_element(driver: WebDriver, element: WebElement) -> None:
        try:
            element.click()
        except (
            AttributeError,
            NoSuchElementException,
            ElementClickInterceptedException,
            ElementNotInteractableException
        ):
            driver.execute_script("arguments[0].click()", element)
        except JavascriptException as je:
            raise Exception("Nao foi possivel executar a funcao") from je

    @staticmethod
    def find_element(
        driver: WebDriver,
        element_locator: str,
        element_type: str = "XPATH") -> None:
        try:
            if element_type == "ID":
                return driver.find_element(By.ID, element_locator)
            elif element_type == "CLASS":
                return driver.find_element(By.CLASS_NAME, element_locator)
            elif element_type == "NAME":
                return driver.find_element(By.NAME, element_locator)
            elif element_type == "TAG":
                return driver.find_element(By.TAG_NAME, element_locator)
            elif element_type == "CSS":
                return driver.find_element(By.CSS_SELECTOR, element_locator)
            elif element_type == "XPATH":
                return driver.find_element(By.XPATH, element_locator)
        except (AttributeError, NoSuchElementException):
            return None

    @staticmethod
    def switch_to_frame(driver, frame_element: WebElement):
        try:
            driver.switch_to.frame(frame_element)
        except NoSuchFrameException as nse:
            raise Exception("Nao foi possivel alterar o frame") from nse
