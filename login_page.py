from __future__ import annotations

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Salesforce Experience Cloud login.

    Username is flaky on this form: password focus / partial page settle can leave
    the email blank. Always re-find fields, verify both values, and refill username
    if it was cleared before submit.
    """

    FILL_RETRIES = 3

    def __init__(self, driver):
        super().__init__(driver, timeout=30)
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

    def navigate_to_login(self, base_url: str) -> None:
        self.driver.get(base_url)
        self._wait_for_visible_field(self.username_locators)
        self._wait_for_visible_field(self.password_locators)
        # Allow Experience Cloud / Aura handlers to attach before interacting.
        time.sleep(1.0)

    def _wait_for_visible_field(self, locators):
        def _find_visible(_driver):
            return self._find_first_visible(locators)

        return self.wait.until(_find_visible)

    def _find_first_visible(self, locators):
        for locator in locators:
            for element in self.driver.find_elements(*locator):
                try:
                    if element.is_displayed() and element.is_enabled():
                        return element
                except Exception:
                    continue
        return None

    def _field_value(self, field) -> str:
        try:
            raw = field.get_attribute("value")
            if raw is not None and str(raw).strip():
                return str(raw).strip()
        except Exception:
            pass
        try:
            via_js = self.driver.execute_script("return arguments[0].value || '';", field)
            return str(via_js or "").strip()
        except Exception:
            return ""

    def _js_set_value(self, field, value: str) -> None:
        """Set value with native setter + events (Aura / Lightning-safe)."""
        self.driver.execute_script(
            """
            const el = arguments[0];
            const val = arguments[1];
            el.focus();
            const proto = window.HTMLInputElement.prototype;
            const descriptor = Object.getOwnPropertyDescriptor(proto, 'value');
            if (descriptor && descriptor.set) {
                descriptor.set.call(el, val);
            } else {
                el.value = val;
            }
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            el.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
            """,
            field,
            value,
        )

    def _set_input_value(self, field, value: str, *, label: str) -> None:
        self.wait.until(lambda _: field.is_displayed() and field.is_enabled())
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", field
        )
        try:
            self.js_click(field)
        except Exception:
            pass
        time.sleep(0.25)

        # Prefer JS set first — more reliable on Salesforce login than send_keys alone.
        self._js_set_value(field, value)
        time.sleep(0.2)

        if self._field_value(field) != value.strip():
            try:
                field.send_keys(Keys.CONTROL, "a")
                field.send_keys(Keys.BACKSPACE)
            except Exception:
                try:
                    field.clear()
                except Exception:
                    pass
            field.send_keys(value)
            time.sleep(0.3)

        if self._field_value(field) != value.strip():
            self._js_set_value(field, value)
            time.sleep(0.2)

        actual = self._field_value(field)
        if actual != value.strip():
            raise ValueError(
                f"Could not populate login {label}. Expected '{value}', got '{actual}'"
            )

    def _fill_credentials(self, user: str, pwd: str) -> None:
        """Fill username then password, and re-check username after password."""
        username_field = self._wait_for_visible_field(self.username_locators)
        self._set_input_value(username_field, user, label="username")

        password_field = self._wait_for_visible_field(self.password_locators)
        self._set_input_value(password_field, pwd, label="password")

        # Password focus / autofill often clears username on this form.
        username_field = self._wait_for_visible_field(self.username_locators)
        if self._field_value(username_field) != user.strip():
            print("[Login] Username was empty/cleared after password fill — refilling.")
            self._set_input_value(username_field, user, label="username")

        password_field = self._wait_for_visible_field(self.password_locators)
        if self._field_value(password_field) != pwd.strip():
            print("[Login] Password missing after username refill — refilling.")
            self._set_input_value(password_field, pwd, label="password")
            # Final username check after second password fill.
            username_field = self._wait_for_visible_field(self.username_locators)
            if self._field_value(username_field) != user.strip():
                self._set_input_value(username_field, user, label="username")

        username_field = self._wait_for_visible_field(self.username_locators)
        password_field = self._wait_for_visible_field(self.password_locators)
        user_actual = self._field_value(username_field)
        pwd_actual = self._field_value(password_field)
        if user_actual != user.strip() or pwd_actual != pwd.strip():
            raise ValueError(
                f"Login fields not ready. username='{user_actual}', "
                f"password_len={len(pwd_actual)} (expected {len(pwd.strip())})"
            )
        print(
            f"[Login] Credentials verified "
            f"(username_len={len(user_actual)}, password_len={len(pwd_actual)})."
        )

    def _find_login_button(self):
        for locator in self.login_button_locators:
            for candidate in self.driver.find_elements(*locator):
                try:
                    if candidate.is_displayed() and candidate.is_enabled():
                        return candidate
                except Exception:
                    continue
        return None

    def login(self, user: str, pwd: str) -> None:
        if not user or not pwd:
            raise ValueError("Login username and password must be non-empty")

        last_error: Exception | None = None
        for attempt in range(1, self.FILL_RETRIES + 1):
            try:
                print(f"[Login] Filling credentials (attempt {attempt}/{self.FILL_RETRIES})...")
                self._fill_credentials(user, pwd)
                last_error = None
                break
            except Exception as exc:
                last_error = exc
                print(f"[Login] Fill attempt {attempt} failed: {exc}")
                time.sleep(1.0)

        if last_error is not None:
            raise last_error

        login_btn = self._find_login_button()
        if login_btn is None:
            raise RuntimeError("Login submit button not found")

        self.wait.until(EC.element_to_be_clickable(login_btn))
        try:
            login_btn.click()
        except Exception:
            self.js_click(login_btn)

        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[title='Dakota Marketplace']")
            )
        )
