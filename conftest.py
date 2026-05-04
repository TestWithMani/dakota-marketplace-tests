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
import shutil
from pathlib import Path
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


def _resolve_browser_binary(browser_name: str) -> str | None:
    env_var_map = {
        "chrome": "CHROME_BINARY",
        "edge": "EDGE_BINARY",
        "firefox": "FIREFOX_BINARY",
    }
    env_var = env_var_map[browser_name]
    explicit_binary = os.environ.get(env_var, "").strip()
    if explicit_binary:
        if not Path(explicit_binary).exists():
            raise FileNotFoundError(
                f"{env_var} is set but file does not exist: {explicit_binary}"
            )
        return explicit_binary

    if browser_name == "chrome":
        names = ["chrome", "google-chrome", "google-chrome-stable", "chrome.exe"]
        candidates = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
    elif browser_name == "edge":
        names = ["msedge", "msedge.exe", "microsoft-edge"]
        candidates = [
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        ]
    else:  # firefox
        names = ["firefox", "firefox.exe"]
        candidates = [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
        ]

    for name in names:
        resolved = shutil.which(name)
        if resolved:
            return resolved
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    return None


def _apply_browser_binary_option(browser_name, options):
    binary = _resolve_browser_binary(browser_name)
    if not binary:
        env_hint = {
            "chrome": "CHROME_BINARY",
            "edge": "EDGE_BINARY",
            "firefox": "FIREFOX_BINARY",
        }[browser_name]
        raise RuntimeError(
            f"Could not find installed {browser_name} browser binary on this machine. "
            f"Install {browser_name} or set {env_hint} to the browser executable path."
        )
    options.binary_location = binary
    logging.info("Using %s binary: %s", browser_name, binary)


@pytest.fixture(scope="function")
def driver(browser_name):
    browser_driver = None

    if browser_name == "chrome":
        options = ChromeOptions()
        _build_common_browser_args(options)
        options.add_argument("--remote-allow-origins=*")  # Chrome 111+ fix
        _apply_browser_binary_option("chrome", options)
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
        _apply_browser_binary_option("edge", options)
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
        _apply_browser_binary_option("firefox", options)
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
