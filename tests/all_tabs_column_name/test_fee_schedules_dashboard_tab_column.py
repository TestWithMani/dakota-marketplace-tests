import time
import allure
from login_page import LoginPage
from config.urls import URLs, get_url
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
@pytest.mark.fee_schedules_dashboard
@pytest.mark.column_names
    @pytest.mark.fa_portal
    @pytest.mark.ria_portal
    @pytest.mark.fo_portal
    @pytest.mark.benchmark_portal
    @pytest.mark.recommends_portal
    @pytest.mark.fa_ria_portal

def test_verify_fee_schedules_dashboard_tab_column_names(driver, base_url, credentials):
    """
    Verify that the columns in the Fee Schedules Dashboard tab match the expected field names.
    Steps:
    1. Log in using provided credentials.
    2. Navigate to the Fee Schedules Dashboard page.
    3. Handle 'Unpin this List View' button if present.
    4. Assert that the table headers match the expected columns.
    5. Take screenshot of the tab just before comparing both lists, and attach it in Allure report.
    """
    print("Step 1: Logging in with provided credentials...")
    username, password = credentials
    login_page = LoginPage(driver)
    login_page.navigate_to_login(base_url)
    login_page.login(username, password)
    print("Login successful.")

    print("Step 2: Navigating to the Fee Schedules Dashboard page...")
    fee_schedules_url = get_url(base_url, URLs.FEE_SCHEDULES_DASHBOARD)
    driver.get(fee_schedules_url)

    print("Waiting for Fee Schedules Dashboard page to load (header visible)...")
    wait = WebDriverWait(driver, 30)
    header_selector = (By.XPATH, "//span[@class='headerTitle']")
    wait.until(EC.visibility_of_element_located(header_selector))
    print("Fee Schedules Dashboard page loaded.")

    print("Step 3: Checking if 'Unpin this List View' button appears and handling it if present...")
    try:
        unpin_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@title='Unpin this List View']"))
        )
        print("'Unpin this List View' button found. Attempting to click using JavaScript to ensure interaction.")
        driver.execute_script("arguments[0].click();", unpin_btn)
        time.sleep(2)

        driver.refresh()
        header_selector = (By.XPATH, "//span[@class='headerTitle']")
        wait.until(EC.visibility_of_element_located(header_selector))
        print("Page refreshed after unpinning.")
    except Exception:
        print("No 'Unpin this List View' button found or error handling it, continuing.")

    print("Step 4: Fetching column header names from the Fee Schedules Dashboard table...")
    field_xpath = "//table[contains(@class,'slds-table')]//span[contains(@class,'slds-truncate') and normalize-space(text())]"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, field_xpath)))
    field_elements = driver.find_elements(By.XPATH, field_xpath)
    actual_headers = [el.text.strip() for el in field_elements if el.text.strip()]

    # Take screenshot and attach to Allure just before comparing both lists
    screenshot_png = driver.get_screenshot_as_png()
    allure.attach(
        screenshot_png,
        name="fee_schedules_dashboard_tab_headers",
        attachment_type=allure.attachment_type.PNG
    )
    print("Screenshot taken and attached to Allure report before asserting column names.")

    print("Actual column headers found:", actual_headers)

    # Update this list to match the actual column names for Fee Schedules Dashboard tab
    expected_headers = [
        "Public Pension Fund",
        "Account",
        "Investment Strategy",
        "Asset Class",
        "Sub-Asset Class",
        "Base Fee",
        "Total Fee"
    ]
    print("Expected column headers for Fee Schedules Dashboard tab:", expected_headers)

    # Compare only the expected number of headers in correct order
    comparison_actual = actual_headers[:len(expected_headers)]
    print("Comparing the first", len(expected_headers), "headers:")
    print("Actual (sliced) headers:", comparison_actual)
    assert comparison_actual == expected_headers, (
        f"Field names do not match!\nExpected: {expected_headers}\nActual: {comparison_actual}"
    )
    print("Test passed: Column names match expected values.")

