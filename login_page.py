from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.username_input = (By.ID, "loginPage:loginForm:login-email")
        self.password_input = (By.ID, "loginPage:loginForm:login-password")
        self.login_button = (By.ID, "loginPage:loginForm:login-submit")

    def navigate_to_login(self, base_url):
        """Navigate to the login page"""
        self.driver.get(base_url)

    def login(self, user, pwd):
        """Login with username and password"""
        # Wait for username field to be present
        username_field = self.wait.until(EC.presence_of_element_located(self.username_input))
        username_field.clear()
        username_field.send_keys(user)
        
        # Wait for password field to be present
        password_field = self.wait.until(EC.presence_of_element_located(self.password_input))
        password_field.clear()
        password_field.send_keys(pwd)
        
        # Wait for login button to be clickable
        login_btn = self.wait.until(EC.element_to_be_clickable(self.login_button))
        login_btn.click()
        
        # Wait for inventory page to load after login
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[title='Dakota Marketplace']")))

