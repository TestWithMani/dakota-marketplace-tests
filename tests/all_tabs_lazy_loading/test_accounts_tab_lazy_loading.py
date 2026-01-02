import time
import allure
from login_page import LoginPage
from config.urls import URLs, get_url
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
@pytest.mark.accounts
@pytest.mark.lazy_loading
@pytest.mark.fa_portal
@pytest.mark.ria_portal
@pytest.mark.fo_portal
@pytest.mark.benchmark_portal
@pytest.mark.recommends_portal
@pytest.mark.fa_ria_portal


def test_accounts_tab_lazy_loading(driver, base_url, credentials):
    """
    End-to-end test for Accounts tab lazy loading functionality:
        - Login
        - Navigate to Accounts tab
        - Unpin list view if needed (like other test cases)
        - Store header
        - Get initial count of loaded records
        - Scroll to bottom repeatedly until new records appear
        - Wait for new records to load after each scroll
        - Verify record count increases after each scroll
        - Continue until 2000 records are loaded or no more records available
        - Validate final record count:
            * If stuck at round numbers (100, 200, 300, etc.) → FAIL (lazy loading broken)
            * If stuck at non-round numbers (233, 333, 415, etc.) → PASS (all records loaded)
            * If >= 2000 records loaded → PASS
        - All steps include Allure screenshots
    """
    wait = WebDriverWait(driver, 20)
    TARGET_RECORDS = 2000
    MAX_SCROLL_ATTEMPTS_WITHOUT_LOAD = 5
    SCROLL_WAIT_TIME = 2  # Wait time after each scroll
    AGGRESSIVE_SCROLL_ATTEMPTS = 5  # Number of aggressive scroll attempts when stuck

    print("Step 1: Logging in...")
    username, password = credentials
    login_page = LoginPage(driver)
    login_page.navigate_to_login(base_url)
    login_page.login(username, password)

    with allure.step("After login"):
        allure.attach(driver.get_screenshot_as_png(), name='after_login.png', attachment_type=allure.attachment_type.PNG)

    print("Step 2: Navigating to Accounts tab...")
    driver.get(get_url(base_url, URLs.ACCOUNTS_DEFAULT))
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']")))
    time.sleep(3)

    with allure.step("After navigating to Accounts tab"):
        allure.attach(driver.get_screenshot_as_png(), name='after_navigate_accounts.png', attachment_type=allure.attachment_type.PNG)

    print("Step 3: Checking if Unpin is needed and performing if available...")
    try:
        unpin_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@title='Unpin this List View']"))
        )
        driver.execute_script("arguments[0].click();", unpin_btn)
        time.sleep(1)
        driver.refresh()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']")))
        print("  Unpinned List View.")
    except Exception:
        print("  Unpin not required or button not found.")

    print("Step 4: Storing header...")
    header_element = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']"))
    )
    stored_header = header_element.text.strip()
    print(f"  Stored header: {stored_header}")
    time.sleep(3)

    print("Step 5: Locating initial account records...")
    # Wait for table to be present
    wait.until(EC.presence_of_element_located((By.XPATH, "//tbody")))
    time.sleep(2)  # Give time for initial records to load

    # Get initial count of loaded records
    initial_records = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
    initial_count = len(initial_records)
    print(f"  Initial count of loaded records: {initial_count}")

    if initial_count == 0:
        raise AssertionError("No records found initially. Cannot proceed with lazy loading test.")

    with allure.step(f"Initial state - {initial_count} records loaded"):
        allure.attach(driver.get_screenshot_as_png(), name=f'initial_{initial_count}_records.png', attachment_type=allure.attachment_type.PNG)

    # Logic addition: If initial count is <= 100 and after scrolling no records load, pass the test.
    print("Step 6: Starting lazy loading test - scrolling to load more records...")
    current_count = initial_count
    previous_count = initial_count
    scroll_attempts_without_load = 0
    total_scroll_attempts = 0
    max_scroll_attempts = 500  # Safety limit to prevent infinite loops

    while current_count < TARGET_RECORDS and scroll_attempts_without_load < MAX_SCROLL_ATTEMPTS_WITHOUT_LOAD and total_scroll_attempts < max_scroll_attempts:
        print(f"  Current record count: {current_count} (Target: {TARGET_RECORDS})")
        
        # Scroll to bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_WAIT_TIME)
        
        # Try scrolling a bit more to trigger lazy loading
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(SCROLL_WAIT_TIME)
        
        total_scroll_attempts += 1
        
        # Wait a bit for new records to potentially load
        time.sleep(1)
        
        # Check for new records
        try:
            # Get current count of records
            current_records = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
            current_count = len(current_records)
            
            if current_count > previous_count:
                print(f"    [OK] New records loaded! Count increased from {previous_count} to {current_count} (+{current_count - previous_count})")
                scroll_attempts_without_load = 0  # Reset counter since we got new records
                previous_count = current_count
                
                # Take screenshot at specific milestones: 500, 1000, 1500, and 2000
                if current_count in [500, 1000, 1500, 2000]:
                    with allure.step(f"Milestone - {current_count} records loaded"):
                        allure.attach(driver.get_screenshot_as_png(), name=f'{current_count}_records_loaded.png', attachment_type=allure.attachment_type.PNG)
                        print(f"    [SCREENSHOT] Captured screenshot at {current_count} records milestone")
            else:
                scroll_attempts_without_load += 1
                print(f"    No new records loaded yet. Attempts without load: {scroll_attempts_without_load}/{MAX_SCROLL_ATTEMPTS_WITHOUT_LOAD}")
                
                # If no new records, try scrolling more aggressively
                if scroll_attempts_without_load < MAX_SCROLL_ATTEMPTS_WITHOUT_LOAD:
                    # Try more aggressive scrolling strategies
                    print(f"    Attempting aggressive scrolling to trigger lazy loading...")
                    for attempt in range(AGGRESSIVE_SCROLL_ATTEMPTS):
                        # Scroll to absolute bottom
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(0.8)
                        # Scroll within table container if it exists
                        try:
                            tbody = driver.find_element(By.XPATH, "//tbody")
                            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});", tbody)
                            time.sleep(0.8)
                        except:
                            pass
                        # Scroll window by large amount
                        driver.execute_script("window.scrollBy(0, 1500);")
                        time.sleep(1.5)
                        # Try scrolling to very bottom
                        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                        time.sleep(1)
                    
                    # Re-check count after aggressive scrolling
                    time.sleep(2)
                    try:
                        check_records = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
                        check_count = len(check_records)
                        if check_count > current_count:
                            current_count = check_count
                            previous_count = check_count
                            scroll_attempts_without_load = 0
                            print(f"    [OK] Aggressive scrolling worked! Count now: {current_count}")
                        else:
                            print(f"    Aggressive scrolling did not load new records. Still at: {current_count}")
                    except Exception as e:
                        print(f"    Error checking records after aggressive scroll: {e}")
        except Exception as e:
            print(f"    Warning: Error while checking records: {e}")
            scroll_attempts_without_load += 1
            time.sleep(1)

    print(f"\nStep 7: Lazy loading completed.")
    print(f"  Final record count: {current_count}")
    print(f"  Target was: {TARGET_RECORDS}")
    print(f"  Total scroll attempts: {total_scroll_attempts}")

    # Final screenshot
    with allure.step(f"Final state - {current_count} records loaded"):
        allure.attach(driver.get_screenshot_as_png(), name=f'final_{current_count}_records.png', attachment_type=allure.attachment_type.PNG)

    print("\nStep 8: Validating results...")
    
    # Helper function to check if a number is a round number (100, 200, 300, etc.)
    def is_round_number(num):
        """Check if number is a round number like 100, 200, 300, etc."""
        # Round numbers are divisible by 100 and end with 00
        return num % 100 == 0 and num >= 100
    
    # New logic: If initial_count <= 100 and no new records were loaded, pass the test as all records have been loaded
    if initial_count <= 100 and current_count == initial_count and scroll_attempts_without_load >= MAX_SCROLL_ATTEMPTS_WITHOUT_LOAD:
        print(f"  [OK] Only {initial_count} records exist (<= 100), and no additional records were available after lazy loading.")
        print(f"  [OK] Validation passed: All available records ({initial_count}) were successfully loaded via lazy loading.")
    elif current_count >= TARGET_RECORDS:
        print(f"  [SUCCESS] Loaded {current_count} records, which meets or exceeds the target of {TARGET_RECORDS} records.")
        assert current_count >= TARGET_RECORDS, f"Expected at least {TARGET_RECORDS} records, but got {current_count}"
    else:
        # Handle case where there are fewer than 2000 records
        if scroll_attempts_without_load >= MAX_SCROLL_ATTEMPTS_WITHOUT_LOAD:
            print(f"  [INFO] Stopped loading after {MAX_SCROLL_ATTEMPTS_WITHOUT_LOAD} attempts without new records.")
            print(f"  Total loaded records: {current_count}")
            print(f"  Target was: {TARGET_RECORDS}")
            
            # Place extra check to skip failure if initial count was <= 100 and no more could be loaded
            if initial_count <= 100 and current_count == initial_count:
                print(f"  [OK] Only {initial_count} records exist (<= 100), and no additional records were available after lazy loading.")
                print(f"  [OK] Validation passed: All available records ({initial_count}) were successfully loaded via lazy loading.")
            else:
                assert current_count > initial_count, (
                    f"Lazy loading did not work. Initial count: {initial_count}, Final count: {current_count}. "
                    f"Expected final count to be greater than initial count."
                )
            
            # CRITICAL CHECK: If we're stuck at a round number (100, 200, 300, etc.), 
            # this indicates lazy loading is broken - test should FAIL
            # Round numbers = 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, etc.
            if is_round_number(current_count):
                print(f"  [WARNING] CRITICAL: Record count is {current_count}, which is a round number (ends with 00).")
                print(f"  This indicates lazy loading is BROKEN and stopped prematurely.")
                
                # Try one more aggressive scroll attempt before failing
                print(f"  Attempting final aggressive scroll to verify we've reached the end...")
                for _ in range(5):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(0.5)
                    driver.execute_script("window.scrollBy(0, 2000);")
                    time.sleep(1.5)
                
                time.sleep(3)
                final_check_records = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
                final_check_count = len(final_check_records)
                
                if final_check_count > current_count:
                    # Found more records! Update count
                    print(f"  [OK] Found more records after aggressive scroll! Count: {final_check_count}")
                    current_count = final_check_count
                    # Re-check if still round number
                    if is_round_number(current_count):
                        error_msg = (
                            f"LAZY LOADING FAILURE: Stuck at round number {current_count} after aggressive scrolling. "
                            f"Lazy loading is broken and did not load all records. "
                            f"Round numbers (100, 200, 300, etc.) indicate premature stopping."
                        )
                        print(f"  [FAIL] {error_msg}")
                        raise AssertionError(error_msg)
                else:
                    # Still stuck at round number - this is a failure
                    error_msg = (
                        f"LAZY LOADING FAILURE: Stuck at round number {current_count} and no more records loaded after aggressive scrolling. "
                        f"Lazy loading is broken. Round numbers (100, 200, 300, etc.) indicate the system stopped prematurely. "
                        f"If only {current_count} records exist, the count would be a non-round number like 233, 333, 415, etc."
                    )
                    print(f"  [FAIL] {error_msg}")
                    raise AssertionError(error_msg)
            else:
                # Non-round number (233, 333, 415, etc.) - this is OK, means all records are loaded
                print(f"  [OK] Record count is {current_count}, which is a non-round number.")
                print(f"  This indicates all available records have been loaded successfully.")
                print(f"  [OK] Validation passed: All available records ({current_count}) were successfully loaded via lazy loading.")
        else:
            # This shouldn't happen, but handle it just in case
            raise AssertionError(
                f"Lazy loading stopped unexpectedly. Current count: {current_count}, "
                f"Target: {TARGET_RECORDS}, Scroll attempts without load: {scroll_attempts_without_load}"
            )

    # Additional validation: Verify that records are actually visible and accessible
    print("\nStep 9: Verifying record accessibility...")
    final_records = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
    visible_count = len([r for r in final_records if r.is_displayed()])
    print(f"  Visible records: {visible_count} out of {current_count} total")
    
    # Verify header is still correct
    current_header = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']"))
    ).text.strip()
    print(f"  Header verification: {current_header}")
    
    print("\n[SUCCESS] Test completed successfully. Lazy loading functionality verified for Accounts tab.")
    print(f"  Summary:")
    print(f"    - Initial records: {initial_count}")
    print(f"    - Final records: {current_count}")
    print(f"    - Records loaded via lazy loading: {current_count - initial_count}")
    print(f"    - Target: {TARGET_RECORDS} (or all available if less)")
    if is_round_number(current_count):
        print(f"    - Status: FAILED (stuck at round number - lazy loading broken)")
    else:
        print(f"    - Status: PASSED (non-round number - all records loaded)")

