import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import os
import logging
from config.settings import resolve_runtime_config

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        help="Browser for UI tests: chrome, edge, firefox",
    )

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
    """Resolved label for ``ENV`` (e.g. ``uat`` or ``uat_fa_data_set``)."""
    runtime = resolve_runtime_config(os.environ.get("ENV"))
    return runtime["environment"]


@pytest.fixture(scope="session")
def portal():
    """Current portal key from ``config.json`` (``all_marketplace_access`` when ``ENV`` is base-only)."""
    runtime = resolve_runtime_config(os.environ.get("ENV"))
    return runtime["portal"]


@pytest.fixture(scope="session")
def runtime_config():
    """Full dict from ``resolve_runtime_config`` (url, credentials, urls map, base_env, portal, …)."""
    return resolve_runtime_config(os.environ.get("ENV"))

@pytest.fixture(scope="session")
def browser_name(request):
    cli_browser = request.config.getoption("--browser")
    browser = (cli_browser or os.environ.get("BROWSER") or "chrome").strip().lower()
    if browser not in {"chrome", "edge", "firefox"}:
        raise ValueError(
            f"Unsupported browser '{browser}'. Supported browsers: chrome, edge, firefox"
        )
    return browser


def _build_common_browser_args(options):
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")


@pytest.fixture(scope="function")
def driver(browser_name):
    browser_driver = None

    if browser_name == "chrome":
        options = ChromeOptions()
        _build_common_browser_args(options)
        options.add_argument("--remote-allow-origins=*")  # Chrome 111+ fix
        try:
            service = ChromeService(ChromeDriverManager().install())
        except Exception as exc:
            logging.warning(
                "ChromeDriverManager failed: %s. Falling back to system ChromeDriver.", exc
            )
            service = ChromeService()
        browser_driver = webdriver.Chrome(service=service, options=options)

    elif browser_name == "edge":
        options = EdgeOptions()
        _build_common_browser_args(options)
        try:
            service = EdgeService(EdgeChromiumDriverManager().install())
        except Exception as exc:
            logging.warning(
                "EdgeDriverManager failed: %s. Falling back to system EdgeDriver.", exc
            )
            service = EdgeService()
        browser_driver = webdriver.Edge(service=service, options=options)

    elif browser_name == "firefox":
        options = FirefoxOptions()
        # Firefox supports a subset of Chromium flags; keep minimal stable options.
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        try:
            service = FirefoxService(GeckoDriverManager().install())
        except Exception as exc:
            logging.warning(
                "GeckoDriverManager failed: %s. Falling back to system geckodriver.", exc
            )
            service = FirefoxService()
        browser_driver = webdriver.Firefox(service=service, options=options)

    if browser_driver is None:
        raise ValueError(f"Driver setup failed for browser '{browser_name}'")

    yield browser_driver
    browser_driver.quit()

@pytest.fixture(scope="function")
def wait(driver):
    """Provides WebDriverWait instance for explicit waits"""
    return WebDriverWait(driver, 30)
