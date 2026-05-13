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

DEFAULT_BROWSER_WIDTH = 1920
DEFAULT_BROWSER_HEIGHT = 1080


def _env_flag(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _resolve_viewport_size() -> tuple[int, int]:
    width_raw = os.environ.get("BROWSER_WIDTH", str(DEFAULT_BROWSER_WIDTH)).strip()
    height_raw = os.environ.get("BROWSER_HEIGHT", str(DEFAULT_BROWSER_HEIGHT)).strip()
    try:
        width = int(width_raw)
        height = int(height_raw)
    except ValueError as exc:
        raise ValueError(
            "BROWSER_WIDTH and BROWSER_HEIGHT must be valid integers."
        ) from exc
    if width <= 0 or height <= 0:
        raise ValueError("BROWSER_WIDTH and BROWSER_HEIGHT must be greater than zero.")
    return width, height


def _is_headless_mode() -> bool:
    # Default to headless on Jenkins unless explicitly overridden.
    default_headless = bool(os.environ.get("JENKINS_URL"))
    return _env_flag("HEADLESS", default=default_headless)


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


def _effective_browser_for_driver(requested: str) -> str:
    """On CI agents without Firefox, fall back to Chrome so jobs do not fail at fixture setup."""
    if requested != "firefox":
        return requested
    if _resolve_browser_binary("firefox") is not None:
        return requested
    ci = _env_flag("CI") or bool(os.environ.get("JENKINS_URL"))
    if ci:
        logging.warning(
            "Requested Firefox but no Firefox binary was found; using Chrome on this agent."
        )
        return "chrome"
    return requested


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
    effective_browser = _effective_browser_for_driver(browser_name)
    browser_driver = None
    viewport_width, viewport_height = _resolve_viewport_size()
    is_headless = _is_headless_mode()

    if effective_browser == "chrome":
        options = ChromeOptions()
        _build_common_browser_args(options)
        options.add_argument(f"--window-size={viewport_width},{viewport_height}")
        if is_headless:
            options.add_argument("--headless=new")
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

    elif effective_browser == "edge":
        options = EdgeOptions()
        _build_common_browser_args(options)
        options.add_argument(f"--window-size={viewport_width},{viewport_height}")
        if is_headless:
            options.add_argument("--headless=new")
        _apply_browser_binary_option("edge", options)
        try:
            service = EdgeService(EdgeChromiumDriverManager().install())
        except Exception as exc:
            logging.warning(
                "EdgeDriverManager failed: %s. Falling back to system EdgeDriver.", exc
            )
            service = EdgeService()
        browser_driver = webdriver.Edge(service=service, options=options)

    elif effective_browser == "firefox":
        options = FirefoxOptions()
        options.add_argument(f"--width={viewport_width}")
        options.add_argument(f"--height={viewport_height}")
        if is_headless:
            options.add_argument("-headless")
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
        raise ValueError(f"Driver setup failed for browser '{effective_browser}'")

    # Enforce viewport after session starts for consistent rendering/click targets.
    browser_driver.set_window_size(viewport_width, viewport_height)

    yield browser_driver
    browser_driver.quit()

@pytest.fixture(scope="function")
def wait(driver):
    """Provides WebDriverWait instance for explicit waits"""
    return WebDriverWait(driver, 30)
