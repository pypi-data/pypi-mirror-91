from selenium.webdriver.chrome.webdriver import WebDriver
from pytest_drivings.base_webdriver import BaseWebDriver


class LocalWebDriver(WebDriver, BaseWebDriver):
    """
    Create local webdrivers using this class to gain access to webdriver helper functions.
    """
