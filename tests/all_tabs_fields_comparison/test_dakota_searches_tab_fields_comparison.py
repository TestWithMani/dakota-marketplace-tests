import time
import allure
import re
import csv
import io
from login_page import LoginPage
from config.urls import URLs, get_url
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest


def generate_fields_comparison_csv(
    select_fields_list,
    additional_filter_fields_list,
    select_fields_normalized,
    additional_filter_normalized,
    only_in_select_fields,
    only_in_additional_filter,
    common_fields,
):
    """
    Generate an in-memory CSV as string for comparison details between two field lists.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    # Write complete list headers
    writer.writerow(["Select Fields To Display fields:"])
    for idx, field in enumerate(select_fields_list, 1):
        writer.writerow([f"{idx}. {field}"])
    writer.writerow([])

    writer.writerow(["Additional Filter fields:"])
    for idx, field in enumerate(additional_filter_fields_list, 1):
        writer.writerow([f"{idx}. {field}"])
    writer.writerow([])

    # Differences
    writer.writerow(["Fields ONLY in 'Select Fields To Display':"])
    if only_in_select_fields:
        for idx, field in enumerate(only_in_select_fields, 1):
            original_field = next((f for f in select_fields_list if f.lower().strip() == field), field)
            writer.writerow([f"{idx}. {original_field}"])
    else:
        writer.writerow(["(none)"])
    writer.writerow([])

    writer.writerow(["Fields ONLY in 'Additional Filter':"])
    if only_in_additional_filter:
        for idx, field in enumerate(only_in_additional_filter, 1):
            original_field = next((f for f in additional_filter_fields_list if f.lower().strip() == field), field)
            writer.writerow([f"{idx}. {original_field}"])
    else:
        writer.writerow(["(none)"])
    writer.writerow([])

    writer.writerow(["Common fields in BOTH lists:"])
    if common_fields:
        for idx, field in enumerate(common_fields, 1):
            # Show from select fields if possible
            original_field = next((f for f in select_fields_list if f.lower().strip() == field), field)
            writer.writerow([f"{idx}. {original_field}"])
    else:
        writer.writerow(["(none)"])
    writer.writerow([])
    return output.getvalue()
@pytest.mark.dakota_searches
@pytest.mark.fields_comparison
    @pytest.mark.fa_portal
    @pytest.mark.ria_portal
    @pytest.mark.fo_portal
    @pytest.mark.benchmark_portal
    @pytest.mark.recommends_portal
    @pytest.mark.fa_ria_portal


def test_dakota_searches_tab_fields_comparison(driver, base_url, credentials):
    """
    End-to-end test for Dakota Searches Tab tab Fields Comparison:
        - Login
        - Take screenshot after login
        - Navigate to Dakota Searches Tab tab
        - Try unpin if present
        - Save header
        - Click on "Select Fields To Display" button
        - Extract fields from the modal and save their names and count
        - Take screenshot
        - Click cancel button
        - Click on additional filter button
        - Click on "Select a Field" button
        - Extract fields from the combobox modal (ignoring "Account:" prefix)
        - Take screenshot
        - Compare both field lists (case insensitive, order independent)
        - All steps include Allure screenshots and csv of comparison
    """
    wait = WebDriverWait(driver, 20)

    print("Step 1: Logging in...")
    username, password = credentials
    login_page = LoginPage(driver)
    login_page.navigate_to_login(base_url)
    login_page.login(username, password)

    # Take screenshot after login
    print("Taking screenshot after login...")
    with allure.step("After Login"):
        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_login",
            attachment_type=allure.attachment_type.PNG
        )

    print("Step 2: Navigating to Dakota Searches Tab tab...")
    driver.get(get_url(base_url, URLs.DAKOTA_SEARCHES_TAB))
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']")))

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
        time.sleep(5)
    except Exception:
        print("  Unpin not required or button not found.")

    print("Step 4: Saving header...")
    original_header = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']"))
    ).text.strip()
    print(f"  Saved header: {original_header}")
    time.sleep(5)

    print("Step 5: Clicking on 'Select Fields To Display' button...")
    select_fields_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@title='Select Fields To Display']"))
    )
    driver.execute_script("arguments[0].click();", select_fields_btn)
    time.sleep(3)

    print("Step 6: Extracting fields from Select Fields To Display modal...")
    field_elements = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//li[@role='presentation']"))
    )
    select_fields_list = []
    for el in field_elements:
        field_text = el.text.strip()
        if field_text:
            select_fields_list.append(field_text)
    
    select_fields_count = len(select_fields_list)
    print(f"  Found {select_fields_count} fields in Select Fields To Display modal")
    print("  Fields list:")
    for idx, field in enumerate(select_fields_list, 1):
        print(f"    {idx}. {field}")

    print("Step 7: Taking screenshot of Select Fields To Display modal...")
    with allure.step("Select Fields To Display modal"):
        allure.attach(
            driver.get_screenshot_as_png(),
            name="select_fields_to_display_modal",
            attachment_type=allure.attachment_type.PNG
        )

    print("Step 8: Clicking on Cancel button...")
    cancel_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'slds-button_neutral') and text()='Cancel']"))
    )
    driver.execute_script("arguments[0].click();", cancel_btn)
    time.sleep(2)

    print("Step 9: Clicking on Additional Filter button...")
    additional_filter_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'additionalFiltersStyling') and .//span[text()='Additional Filtering']]"))
    )
    driver.execute_script("arguments[0].click();", additional_filter_btn)
    time.sleep(2)

    print("Step 10: Clicking on 'Select a Field' button...")
    select_field_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Select a Field']"))
    )
    driver.execute_script("arguments[0].click();", select_field_btn)
    time.sleep(2)

    print("Step 11: Extracting fields from Additional Filter combobox modal...")
    combobox_elements = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//lightning-base-combobox-item[contains(@class, 'slds-listbox__option')]"))
    )
    additional_filter_fields_list = []
    for el in combobox_elements:
        field_text = el.text.strip()
        if field_text:
            # Remove "Account:" prefix if present (case insensitive)
            # Handle patterns like "Account: AUM", "Account: Type", etc.
            if re.match(r'^Account:\s*', field_text, re.IGNORECASE):
                # Remove "Account:" prefix and any whitespace after colon
                field_text = re.sub(r'^Account:\s*', '', field_text, flags=re.IGNORECASE).strip()
            additional_filter_fields_list.append(field_text)
    
    additional_filter_count = len(additional_filter_fields_list)
    print(f"  Found {additional_filter_count} fields in Additional Filter combobox")
    print("  Fields list:")
    for idx, field in enumerate(additional_filter_fields_list, 1):
        print(f"    {idx}. {field}")

    print("Step 12: Taking screenshot of Additional Filter combobox modal...")
    with allure.step("Additional Filter combobox modal"):
        allure.attach(
            driver.get_screenshot_as_png(),
            name="additional_filter_combobox_modal",
            attachment_type=allure.attachment_type.PNG
        )

    print("Step 13: Comparing both field lists (case insensitive, order independent)...")
    print("=" * 80)
    
    # Normalize both lists: convert to lowercase and sort for comparison
    select_fields_normalized = sorted([field.lower().strip() for field in select_fields_list if field.strip()])
    additional_filter_normalized = sorted([field.lower().strip() for field in additional_filter_fields_list if field.strip()])
    
    print(f"\nSUMMARY:")
    print(f"  Select Fields To Display: {select_fields_count} fields")
    print(f"  Additional Filter fields: {additional_filter_count} fields")
    
    # Find differences
    only_in_select_fields = sorted(list(set(select_fields_normalized) - set(additional_filter_normalized)))
    only_in_additional_filter = sorted(list(set(additional_filter_normalized) - set(select_fields_normalized)))
    common_fields = sorted(list(set(select_fields_normalized) & set(additional_filter_normalized)))
    
    print(f"  Common fields: {len(common_fields)}")
    print(f"  Fields only in Select Fields To Display: {len(only_in_select_fields)}")
    print(f"  Fields only in Additional Filter: {len(only_in_additional_filter)}")
    print("=" * 80)

    # --- Save CSV details to Allure ---
    csv_content = generate_fields_comparison_csv(
        select_fields_list,
        additional_filter_fields_list,
        select_fields_normalized,
        additional_filter_normalized,
        only_in_select_fields,
        only_in_additional_filter,
        common_fields,
    )
    with allure.step("Attach CSV fields comparison to Allure report"):
        allure.attach(
            csv_content,
            name="dakota_searches_tab_fields_comparison.csv",
            attachment_type=allure.attachment_type.CSV
        )
    # ---

    # Print detailed comparison
    if only_in_select_fields or only_in_additional_filter:
        print("\nFIELD MISMATCH DETECTED!")
        print("=" * 80)
        
        if only_in_select_fields:
            print(f"\nFields ONLY in 'Select Fields To Display' ({len(only_in_select_fields)} fields):")
            for idx, field in enumerate(only_in_select_fields, 1):
                # Find original case version
                original_field = next((f for f in select_fields_list if f.lower().strip() == field), field)
                print(f"  {idx}. {original_field}")
        
        if only_in_additional_filter:
            print(f"\nFields ONLY in 'Additional Filter' ({len(only_in_additional_filter)} fields):")
            for idx, field in enumerate(only_in_additional_filter, 1):
                # Find original case version
                original_field = next((f for f in additional_filter_fields_list if f.lower().strip() == field), field)
                print(f"  {idx}. {original_field}")
        
        if common_fields:
            print(f"\nCommon fields found in BOTH lists ({len(common_fields)} fields):")
            for idx, field in enumerate(common_fields, 1):
                # Find original case version from select fields
                original_field = next((f for f in select_fields_list if f.lower().strip() == field), field)
                print(f"  {idx}. {original_field}")
        
        print("\n" + "=" * 80)
        print("COMPLETE FIELD LISTS:")
        print("=" * 80)
        print(f"\n'Select Fields To Display' - Complete list ({select_fields_count} fields):")
        for idx, field in enumerate(select_fields_list, 1):
            print(f"  {idx}. {field}")
        
        print(f"\n'Additional Filter' - Complete list ({additional_filter_count} fields):")
        for idx, field in enumerate(additional_filter_fields_list, 1):
            print(f"  {idx}. {field}")
        print("=" * 80)
    else:
        print("\n✓ All fields match! Both lists contain the same fields.")
        print(f"\nAll {len(common_fields)} fields are present in both lists:")
        for idx, field in enumerate(common_fields, 1):
            original_field = next((f for f in select_fields_list if f.lower().strip() == field), field)
            print(f"  {idx}. {original_field}")
    
    # Assert that both lists contain the same fields (order independent, case insensitive)
    assert select_fields_normalized == additional_filter_normalized, (
        f"\n{'='*80}\n"
        f"FIELD COMPARISON FAILED\n"
        f"{'='*80}\n"
        f"Select Fields To Display: {select_fields_count} fields\n"
        f"Additional Filter fields: {additional_filter_count} fields\n"
        f"\nFields ONLY in 'Select Fields To Display': {len(only_in_select_fields)}\n"
        f"{chr(10).join(f'  - {next((f for f in select_fields_list if f.lower().strip() == field), field)}' for field in only_in_select_fields) if only_in_select_fields else '  (none)'}\n"
        f"\nFields ONLY in 'Additional Filter': {len(only_in_additional_filter)}\n"
        f"{chr(10).join(f'  - {next((f for f in additional_filter_fields_list if f.lower().strip() == field), field)}' for field in only_in_additional_filter) if only_in_additional_filter else '  (none)'}\n"
        f"{'='*80}"
    )
    
    print("\n✓ Test completed successfully. Both field lists match (case insensitive, order independent).")

