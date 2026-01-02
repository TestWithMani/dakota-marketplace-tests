import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import os
import json
import logging

# Load environment-specific configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "config.json")
with open(CONFIG_PATH) as f:
    config = json.load(f)

@pytest.fixture(scope="session")
def base_url():
    # Support both old format (uat/prod) and new format (uat_fa_portal, prod_ria_portal, etc.)
    env = os.environ.get("ENV", "uat")  # default to original uat
    # If old format is used (uat/prod), use as-is (no portal suffix)
    # If new format is used (uat_fa_portal, etc.), use as-is
    if env not in ["uat", "prod"] and not env.startswith(("uat_", "prod_")):
        # Fallback: if invalid format, use uat
        env = "uat"
    
    if env not in config:
        raise ValueError(f"Configuration not found for environment: {env}. Available: {list(config.keys())}")
    return config[env]["url"]

@pytest.fixture(scope="session")
def credentials():
    # Support both old format (uat/prod) and new format (uat_fa_portal, prod_ria_portal, etc.)
    env = os.environ.get("ENV", "uat")  # default to original uat
    # If old format is used (uat/prod), use as-is (no portal suffix)
    # If new format is used (uat_fa_portal, etc.), use as-is
    if env not in ["uat", "prod"] and not env.startswith(("uat_", "prod_")):
        # Fallback: if invalid format, use uat
        env = "uat"
    
    if env not in config:
        raise ValueError(f"Configuration not found for environment: {env}. Available: {list(config.keys())}")
    return config[env]["username"], config[env]["password"]

@pytest.fixture(scope="session")
def environment():
    """Get the current environment name"""
    env = os.environ.get("ENV", "uat")  # default to original uat
    # If old format is used (uat/prod), use as-is (no portal suffix)
    # If new format is used (uat_fa_portal, etc.), use as-is
    if env not in ["uat", "prod"] and not env.startswith(("uat_", "prod_")):
        # Fallback: if invalid format, use uat
        env = "uat"
    return env

@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--remote-allow-origins=*")  # Chrome 111+ fix

    # Setup ChromeDriver
    try:
        # Use ChromeDriverManager to automatically download and manage ChromeDriver
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
    except Exception as e:
        # Fallback: let Selenium find ChromeDriver automatically
        logging.warning(f"ChromeDriverManager failed: {e}. Using system ChromeDriver.")
        service = Service()
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def wait(driver):
    """Provides WebDriverWait instance for explicit waits"""
    return WebDriverWait(driver, 30)
