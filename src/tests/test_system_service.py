from unittest.mock import MagicMock, patch

import pytest

from src.services.system_service import SystemService
from src.utils.constants import (
    LOGIN_ERROR,
    LOGIN_SUCCESS,
)


@pytest.fixture
def driver():
    return MagicMock()

@pytest.fixture(autouse=True)
def env_vars(monkeypatch):
    monkeypatch.setenv("ACCESS_URL", "http://test-url")
    monkeypatch.setenv("ACCESS_USER", "user@test.com")
    monkeypatch.setenv("ACCESS_PASSWORD", "123456")

@patch("src.services.system_service.Selenium")
def test_login_success(mock_selenium, driver):
    mock_selenium.wait_element_exists.side_effect = [
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
    ]

    service = SystemService(driver)
    response = service.login()

    assert response["status"] is True
    assert response["message"] == LOGIN_SUCCESS

@patch("src.services.system_service.Selenium")
def test_login_error(mock_selenium, driver):
    mock_selenium.wait_element_exists.side_effect = [
        MagicMock(),
        MagicMock(),
        MagicMock(),
        None,
    ]

    service = SystemService(driver)
    response = service.login()

    assert response["status"] is False
    assert LOGIN_ERROR in response["message"]

@patch("src.services.system_service.Selenium")
def test_logout_success(mock_selenium, driver):
    mock_selenium.wait_element_exists.side_effect = [
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
    ]

    service = SystemService(driver)
    response = service.logout()

    assert response is True

@patch("src.services.system_service.Selenium")
def test_logout_error(mock_selenium, driver):
    mock_selenium.wait_element_exists.side_effect = [
        MagicMock(),
        MagicMock(),
        MagicMock(),
        None,
    ]

    service = SystemService(driver)
    response = service.logout()

    assert response is False
