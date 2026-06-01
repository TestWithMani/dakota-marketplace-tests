from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.username_locators = [
            (By.ID, "loginPage:loginForm:login-email"),
            (By.NAME, "username"),
            (By.CSS_SELECTOR, "input[type='email']"),
            (By.CSS_SELECTOR, "input[autocomplete='username']"),
        ]
        self.password_locators = [
            (By.ID, "loginPage:loginForm:login-password"),
            (By.NAME, "password"),
            (By.CSS_SELECTOR, "input[type='password']"),
            (By.CSS_SELECTOR, "input[autocomplete='current-password']"),
        ]
        self.login_button_locators = [
            (By.ID, "loginPage:loginForm:login-submit"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.CSS_SELECTOR, "input[type='submit']"),
            (By.XPATH, "//button[contains(.,'Log In') or contains(.,'Login')]"),
        ]

    def navigate_to_login(self, base_url):
        """Navigate to the login page"""
        self.driver.get(base_url)

    def _find_first_present(self, locators):
        for locator in locators:
            elements = self.driver.find_elements(*locator)
            if elements:
                return locator
        return None

    def _set_input_value(self, locator, value):
        field = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", field)
        try:
            field.clear()
            field.send_keys(value)
            if field.get_attribute("value") != value:
                raise ValueError("send_keys did not populate field value")
        except Exception:
            # JS fallback for dynamic inputs where send_keys is swallowed.
            self.driver.execute_script(
                "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', {bubbles:true})); arguments[0].dispatchEvent(new Event('change', {bubbles:true}));",
                field,
                value,
            )

    def login(self, user, pwd):
        """Login with username and password"""
        username_locator = self.wait.until(lambda d: self._find_first_present(self.username_locators))
        password_locator = self.wait.until(lambda d: self._find_first_present(self.password_locators))

        self._set_input_value(username_locator, user)
        self._set_input_value(password_locator, pwd)

        login_locator = self.wait.until(lambda d: self._find_first_present(self.login_button_locators))
        login_btn = self.wait.until(EC.element_to_be_clickable(login_locator))
        login_btn.click()
        
        # Wait for inventory page to load after login
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[title='Dakota Marketplace']")))

