import os

# Template for test files
template = '''import time
import allure
import random
import re
from login_page import LoginPage
from config.urls import URLs, get_url
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_all_move_buttons(driver, move_btn_xpaths):
    """
    Click each button in move_btn_xpaths (ignores missing/non-clickable).
    """
    for xpath in move_btn_xpaths:
        try:
            btn = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.5)
        except Exception:
            pass

def test_{test_name}_fields_display_functionality(driver, base_url, credentials):
    """
    End-to-end validation for the {tab_display_name} tab fields display functionality.
    Test Steps:
      1. Log in and capture the state.
      2. Navigate to the target tab.
      3. Unpin default list view, if present.
      4. Capture and print original table column headers.
      5. Open 'Select Fields To Display' and fetch all field names.
      6. Move the last field to 'Available', first field to 'Selected'.
      7. Confirm changes with 'Add' button.
      8. Create a new list view and verify header.
      9. Confirm change in table headers (at least one diff).
      10. Clean up by deleting the custom list view.
    Test fails if no header diff is detected after the steps.
    """

    wait = WebDriverWait(driver, 20)

    # Step 1: Login
    print("[Step 1] Logging in to the application...")
    username, password = credentials
    login_page = LoginPage(driver)
    login_page.navigate_to_login(base_url)
    login_page.login(username, password)
    with allure.step("After Login"):
        allure.attach(driver.get_screenshot_as_png(), name="after_login", attachment_type=allure.attachment_type.PNG)
    print("[✓] Login successful and screenshot taken.")

    # Step 2: Navigate to {tab_display_name} Tab
    print("[Step 2] Navigating to {tab_display_name} tab...")
    driver.get(get_url(base_url, URLs.{url_constant}))
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']")))
    time.sleep(2)
    print("[✓] {tab_display_name} tab loaded.")

    # Step 3: Try Unpin
    print("[Step 3] Checking for 'Unpin this List View' button...")
    try:
        unpin_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@title='Unpin this List View']"))
        )
        driver.execute_script("arguments[0].click();", unpin_btn)
        time.sleep(1)
        driver.refresh()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']")))
        print("[✓] List view unpinned and page refreshed.")
        time.sleep(2)
    except Exception:
        print("[i] No unpin needed (button not found or already unpinned).")

    # Step 4: Save Current Header
    print("[Step 4] Capturing original header for verification...")
    original_header = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']"))
    ).text.strip()
    print(f"    Original List View Name: {{original_header}}")
    time.sleep(1)

    # Step 4a: Save table column headers BEFORE field selection change
    print("[Step 4a] Saving table column headers BEFORE changing display fields:")
    header_span_elems = driver.find_elements(By.XPATH, "//th[@role='columnheader']//span[contains(@class,'slds-truncate')]")
    original_column_names = [elem.text.strip() for elem in header_span_elems if elem.text.strip()]
    if not original_column_names:
        raise AssertionError("No table column headers found before changing Select Fields To Display.")
    print(f"    ({{len(original_column_names)}}) columns: {{', '.join(original_column_names)}}")

    # Step 5: Open Select Fields To Display
    print("[Step 5] Opening 'Select Fields To Display' dialog...")
    select_fields_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Select Fields To Display']")))
    driver.execute_script("arguments[0].click();", select_fields_btn)
    time.sleep(2)

    # Step 6: Scrape all field names from modal
    print("[Step 6] Fetching available fields for display selection...")
    field_elements = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//li[@role='presentation']"))
    )
    fields_list = [el.text.strip() for el in field_elements if el.text.strip()]
    print(f"    Total fields found: {{len(fields_list)}}")
    if not fields_list:
        raise AssertionError("No fields found in Select Fields To Display modal")
    print("    Fields available:", ', '.join(fields_list))

    # Get first and last for further operations
    first_field_name = fields_list[0]
    last_field_name = fields_list[-1]
    print(f"    Candidate for moving - First: \\"{{first_field_name}}\\", Last: \\"{{last_field_name}}\\"")

    # Step 7: Move LAST field to Available
    print("[Step 7] Moving LAST field to Available Fields...")
    last_field_xpath = f"(//li[@role='presentation'])[{{len(fields_list)}}]"
    last_field_element = wait.until(EC.element_to_be_clickable((By.XPATH, last_field_xpath)))
    driver.execute_script("arguments[0].scrollIntoView({{block: 'center'}});", last_field_element)
    time.sleep(0.4)
    last_field_element.click()
    time.sleep(0.6)
    move_to_available_xpaths = [
        "(//button[@title='Move to Available Fields'])[1]",
        "(//button[@title='Move to Available Fields'])[2]",
        "(//button[@title='Move to Selected Visible Fields'])[1]",
        "(//button[@title='Move to Selected Visible Fields'])[2]"
    ]
    click_all_move_buttons(driver, move_to_available_xpaths)
    time.sleep(0.8)
    print(f"    Last field '{{last_field_name}}' moved to Available Fields.")

    # Step 7a: Move FIRST field to Selected
    print("[Step 8] Moving FIRST field to Selected Visible Fields...")
    first_field_xpath = "(//li[@role='presentation'])[1]"
    first_field_element = wait.until(EC.element_to_be_clickable((By.XPATH, first_field_xpath)))
    driver.execute_script("arguments[0].scrollIntoView({{block: 'center'}});", first_field_element)
    time.sleep(0.4)
    first_field_element.click()
    time.sleep(0.6)
    move_to_selected_visible_xpaths = [
        "(//button[@title='Move to Available Fields'])[1]",
        "(//button[@title='Move to Available Fields'])[2]",
        "(//button[@title='Move to Selected Visible Fields'])[1]",
        "(//button[@title='Move to Selected Visible Fields'])[2]"
    ]
    click_all_move_buttons(driver, move_to_selected_visible_xpaths)
    time.sleep(0.8)
    print(f"    First field '{{first_field_name}}' re-added to Selected Visible Fields.")

    # Step 9: Screenshot before Add
    print("[Step 9] Screenshot before confirming display changes (Add)...")
    with allure.step("Before clicking Add button"):
        allure.attach(
            driver.get_screenshot_as_png(),
            name="before_add_button",
            attachment_type=allure.attachment_type.PNG
        )

    # Step 10: Click Add, apply changes
    print("[Step 10] Clicking Add button to confirm displayed columns...")
    add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add']")))
    add_btn.click()
    print("    Add button clicked.")
    time.sleep(6)

    # Step 11: Create new list view (Save As)
    print("[Step 11] Performing 'Save As' to create a custom list view...")
    save_as_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space(.)='Save As'])[1]"))
    )
    driver.execute_script("arguments[0].click();", save_as_btn)
    time.sleep(2)
    new_list_view_name = f"Automation by Mani {{random.randint(1000, 9999)}}"
    print(f"    Created List View Name: {{new_list_view_name}}")

    name_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='enter-list-view-name']"))
    )
    name_input.clear()
    name_input.send_keys(new_list_view_name)

    save_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space(.)='Save'])[2]"))
    )
    driver.execute_script("arguments[0].click();", save_btn)
    time.sleep(6)

    saved_header = WebDriverWait(driver, 12).until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']"))
    ).text.strip()
    saved_base = re.split(r'\\s*\\(', saved_header, 1)[0].strip()
    assert saved_base == new_list_view_name, f"Saved list view name mismatch: {{saved_base}} != {{new_list_view_name}}"
    print(f"    [✓] New list view '{{saved_base}}' saved and loaded.")

    with allure.step(f"After save as new list view: {{new_list_view_name}}"):
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f'{{new_list_view_name}}_after_save.png',
            attachment_type=allure.attachment_type.PNG
        )

    # Step 12: Table header check (main logic)
    print("[Step 12] Verifying that table headers have CHANGED after field selection...")
    wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'slds-table')]")))
    time.sleep(2)
    header_span_elems_new = driver.find_elements(By.XPATH, "//th[@role='columnheader']//span[contains(@class,'slds-truncate')]")
    new_column_names = [elem.text.strip() for elem in header_span_elems_new if elem.text.strip()]
    if not new_column_names:
        raise AssertionError("No table column headers found after changing Select Fields To Display.")

    set_original = set(original_column_names)
    set_new = set(new_column_names)
    missing_in_new = set_original - set_new
    added_in_new = set_new - set_original

    # Pretty print the diff
    print(f"    Old columns ({{len(original_column_names)}}): {{', '.join(original_column_names)}}")
    print(f"    New columns ({{len(new_column_names)}}): {{', '.join(new_column_names)}}")
    if missing_in_new:
        print("    [Removed columns]:", ', '.join(sorted(missing_in_new)))
    if added_in_new:
        print("    [Added columns]:", ', '.join(sorted(added_in_new)))

    if missing_in_new or added_in_new:
        print("    [✓] Table columns CHANGED - test PASSED.")
    else:
        print("    [X] Table columns did NOT change - test FAILED!")
        raise AssertionError("No change in table column headers after list view save: expected at least one difference.")

    # Step 13: Screenshot after verification
    print("[Step 13] Screenshot after verifying field display diff.")
    with allure.step("After field display verification"):
        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_field_display_verification",
            attachment_type=allure.attachment_type.PNG
        )

    # Step 14: Delete the custom list view
    print(f"[Step 14] Deleting the created list view '{{new_list_view_name}}' for cleanup...")
    delete_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//svg[@data-key='delete'] or contains(@title,'Delete') or .//span[contains(normalize-space(.),'Delete')]]"))
    )
    driver.execute_script("arguments[0].click();", delete_btn)
    confirm_delete_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[contains(text(),'Delete')])"))
    )
    driver.execute_script("arguments[0].click();", confirm_delete_btn)
    time.sleep(12)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']")))

    select_list_view_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@title='Select a List View']"))
    )
    driver.execute_script("arguments[0].click();", select_list_view_btn)
    time.sleep(1.2)
    views_after_delete = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@role='main']//li//a[1]"))
    )
    names_after = [el.text.strip() for el in views_after_delete]
    assert new_list_view_name not in names_after, f"List view '{{new_list_view_name}}' still appears after deletion"
    print(f"    [✓] List view '{{new_list_view_name}}' was deleted successfully and no longer appears.")

    with allure.step(f"After deletion - list view removed: {{new_list_view_name}}"):
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f'after_delete_verification.png',
            attachment_type=allure.attachment_type.PNG
        )

    # Final
    print("\\n[✔] Test completed successfully. Summary:")
    print(f"    - Original columns: {{', '.join(original_column_names)}}")
    print(f"    - Columns after change: {{', '.join(new_column_names)}}")
    print(f"    - Custom list view '{{new_list_view_name}}' was created and deleted as part of verification.")
'''

# List of all tabs (excluding FILINGS_13F_INVESTMENTS_SEARCH_TAB which already exists)
# Also excluding ACCOUNTS_DEFAULT, CONTACT_DEFAULT, INVESTMENT_ALLOCATOR_ACCOUNTS_DEFAULT which we already created
tabs = [
    ('INVESTMENT_FIRM_ACCOUNTS_DEFAULT', 'Investment Firm Accounts Default', 'investment_firm_accounts_default'),
    ('DAKOTA_SEARCHES_TAB', 'Dakota Searches', 'dakota_searches_tab'),
    ('MY_ACCOUNTS_DEFAULT', 'My Accounts Default', 'my_accounts_default'),
    ('INVESTMENT_ALLOCATOR_CONTACTS_DEFAULT', 'Investment Allocator Contacts Default', 'investment_allocator_contacts_default'),
    ('INVESTMENT_FIRM_CONTACTS_DEFAULT', 'Investment Firm Contacts Default', 'investment_firm_contacts_default'),
    ('PORTFOLIO_COMPANIES_CONTACTS_DEFAULT', 'Portfolio Companies Contacts Default', 'portfolio_companies_contacts_default'),
    ('UNIVERSITY_ALUMNI_CONTACTS_DEFAULT', 'University Alumni Contacts Default', 'university_alumni_contacts_default'),
    ('ALL_DOCUMENTS', 'All Documents', 'all_documents'),
    ('MANAGER_PRESENTATION_DASHBOARD', 'Manager Presentation Dashboard', 'manager_presentation_dashboard'),
    ('CONSULTANT_REVIEWS', 'Consultant Reviews', 'consultant_reviews'),
    ('PENSION_DOCUMENTS', 'Pension Documents', 'pension_documents'),
    ('PUBLIC_PLAN_MINUTES_SEARCH_TAB', 'Public Plan Minutes Search', 'public_plan_minutes_search_tab'),
    ('FEE_SCHEDULES_DASHBOARD', 'Fee Schedules Dashboard', 'fee_schedules_dashboard'),
    ('FUND_FAMILY_MEMOS', 'Fund Family Memos', 'fund_family_memos'),
    ('DAKOTA_CITY_GUIDES', 'Dakota City Guides', 'dakota_city_guides'),
    ('PUBLIC_INVESTMENTS_SEARCH_TAB', 'Public Investments Search', 'public_investments_search_tab'),
    ('PRIVATE_FUND_SEARCH_TAB', 'Private Fund Search', 'private_fund_search_tab'),
    ('FUND_LAUNCHES', 'Fund Launches', 'fund_launches'),
    ('CONTINUATION_VEHICLE', 'Continuation Vehicle', 'continuation_vehicle'),
    ('PORTFOLIO_COMPANIES', 'Portfolio Companies', 'portfolio_companies'),
    ('RECENT_TRANSACTIONS', 'Recent Transactions', 'recent_transactions'),
    ('CONFERENCE_SEARCH_TAB', 'Conference Search', 'conference_search_tab'),
    ('DAKOTA_VIDEO_SEARCH_TAB', 'Dakota Video Search', 'dakota_video_search_tab'),
    ('PUBLIC_COMPANY_SEARCH_TAB', 'Public Company Search', 'public_company_search_tab'),
]

# Change to the test directory
test_dir = 'tests/all_tabs_fields_display_functionality'
os.chdir(test_dir)

# Generate files
for url_constant, tab_display_name, test_name in tabs:
    filename = f'test_{test_name}_fields_display.py'
    if not os.path.exists(filename):
        content = template.format(
            test_name=test_name,
            tab_display_name=tab_display_name,
            url_constant=url_constant
        )
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Created: {filename}')
    else:
        print(f'Skipped (exists): {filename}')

print(f'\nTotal files processed: {len(tabs)}')

