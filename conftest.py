import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import os
import logging
from config.settings import resolve_runtime_config

@pytest.fixture(scope="session")
def base_url():
    runtime = resolve_runtime_config(os.environ.get("ENV"))
    return runtime["url"]

@pytest.fixture(scope="session")
def credentials():
    runtime = resolve_runtime_config(os.environ.get("ENV"))
    return runtime["username"], runtime["password"]

@pytest.fixture(scope="session")
def environment():
    """Get the current environment name"""
    runtime = resolve_runtime_config(os.environ.get("ENV"))
    return runtime["environment"]

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
