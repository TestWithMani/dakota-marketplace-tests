from __future__ import annotations

from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Common Selenium helpers shared by page objects."""

    def __init__(self, driver, timeout: int = 30):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def js_click(self, element) -> None:
        """Click via JavaScript to bypass overlay/animation intercepts."""
        self.driver.execute_script("arguments[0].click();", element)
