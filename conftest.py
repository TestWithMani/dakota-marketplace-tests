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
import re
import threading
import time
import uuid
from pathlib import Path

import allure
import imageio
import mss
import numpy as np
from config.settings import resolve_runtime_config

VIDEO_DIR = Path("reports") / "videos"
VIDEO_FPS = 6
VIDEO_CODEC = "libx264"


class _TestVideoRecorder:
    def __init__(self, driver, output_path):
        self.driver = driver
        self.output_path = output_path
        self._stop_event = threading.Event()
        self._thread = None
        self._writer = None
        self._error = None

    def start(self):
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self._writer = imageio.get_writer(
            str(self.output_path),
            fps=VIDEO_FPS,
            codec=VIDEO_CODEC,
            quality=6,
            macro_block_size=None,
        )
        self._thread = threading.Thread(target=self._record_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=3)
        if self._writer:
            self._writer.close()

    def _record_loop(self):
        with mss.mss() as screen:
            while not self._stop_event.is_set():
                try:
                    rect = self.driver.get_window_rect()
                    monitor = {
                        "left": max(int(rect.get("x", 0)), 0),
                        "top": max(int(rect.get("y", 0)), 0),
                        "width": max(int(rect.get("width", 1)), 1),
                        "height": max(int(rect.get("height", 1)), 1),
                    }
                    frame = np.array(screen.grab(monitor))
                    # Convert BGRA -> RGB for encoder
                    frame = frame[:, :, :3][:, :, ::-1]
                    self._writer.append_data(frame)
                except Exception as exc:
                    self._error = exc
                    break
                time.sleep(1 / VIDEO_FPS)


def _safe_test_name(nodeid):
    name = re.sub(r"[^a-zA-Z0-9_.-]+", "_", nodeid)
    return name[:160]

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
    """Get the current environment name"""
    runtime = resolve_runtime_config(os.environ.get("ENV"))
    return runtime["environment"]

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


@pytest.fixture(scope="function", autouse=True)
def attach_test_video_to_allure(request, driver):
    """
    Record every test and always attach video to Allure.
    Works for pass/fail/skip as teardown always executes.
    """
    video_name = f"{_safe_test_name(request.node.nodeid)}_{uuid.uuid4().hex[:8]}.mp4"
    video_path = VIDEO_DIR / video_name
    recorder = _TestVideoRecorder(driver, video_path)

    try:
        recorder.start()
    except Exception as exc:
        logging.warning("Video recorder failed to start for %s: %s", request.node.nodeid, exc)
        recorder = None

    yield

    if recorder:
        try:
            recorder.stop()
        except Exception as exc:
            logging.warning("Video recorder failed to stop for %s: %s", request.node.nodeid, exc)

        if recorder._error:
            logging.warning("Video recorder runtime error for %s: %s", request.node.nodeid, recorder._error)

    if video_path.exists() and video_path.stat().st_size > 0:
        allure.attach.file(
            str(video_path),
            name=f"Test Video - {request.node.name}",
            attachment_type=allure.attachment_type.MP4,
        )
