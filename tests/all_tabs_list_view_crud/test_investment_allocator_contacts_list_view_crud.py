import time
import allure
import re
import random
from login_page import LoginPage
from config.urls import URLs, get_url
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
@pytest.mark.investment_allocator_contacts
@pytest.mark.list_view_crud
    @pytest.mark.fa_portal
    @pytest.mark.ria_portal
    @pytest.mark.fo_portal
    @pytest.mark.benchmark_portal
    @pytest.mark.recommends_portal
    @pytest.mark.fa_ria_portal


def test_investment_allocator_contacts_list_view_crud(driver, base_url, credentials):
    """
    End-to-end test for Investment Allocator Contacts tab List View:
        - Unpinning if necessary
        - Save As (create) new list view
        - Verify unchanged columns
        - Rename list view
        - Delete list view
        - Verify delete
        - All steps include Allure screenshots
    """
    wait = WebDriverWait(driver, 20)

    print("Step 1: Logging in...")
    username, password = credentials
    login_page = LoginPage(driver)
    login_page.navigate_to_login(base_url)
    login_page.login(username, password)

    print("Step 2: Navigating to Investment Allocator Contacts tab...")
    driver.get(get_url(base_url, URLs.INVESTMENT_ALLOCATOR_CONTACTS_DEFAULT))
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
    except Exception:
        print("  Unpin not required or button not found.")

    print("Step 4: Grabbing original header/base...")
    original_header = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']"))
    ).text.strip()
    original_base = re.split(r'\s*\(', original_header, 1)[0].strip()
    time.sleep(1)

    print("Step 5: Collecting original columns/texts...")
    initial_cols = [el.text.strip() for el in driver.find_elements(By.XPATH, "//div[@class='slds-truncate']")]

    print("Screenshot: Before saving a list view")
    with allure.step("Before saving new Investment Allocator Contacts list view"):
        allure.attach(driver.get_screenshot_as_png(), attachment_type=allure.attachment_type.PNG)

    print("Step 6: Performing 'Save As' for new list view...")
    save_as_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space(.)=\'Save As\'])[1]"))
    )
    driver.execute_script("arguments[0].click();", save_as_btn)
    time.sleep(3)
    new_list_view_name = f"Automation by Mani {random.randint(1000, 9999)}"
    print(f"  New List View Name: {new_list_view_name}")

    name_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='enter-list-view-name']"))
    )
    name_input.clear()
    name_input.send_keys(new_list_view_name)

    save_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space(.)=\'Save\'])[2]"))
    )
    driver.execute_script("arguments[0].click();", save_btn)
    time.sleep(6)

    print("  Checking if the new list view loads with correct name...")
    saved_header = WebDriverWait(driver, 12).until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']"))
    ).text.strip()
    saved_base = re.split(r'\s*\(', saved_header, 1)[0].strip()
    assert saved_base == new_list_view_name

    with allure.step(f"After save as new list view: {new_list_view_name}"):
        allure.attach(driver.get_screenshot_as_png(), name=f'{new_list_view_name}_after_save.png', attachment_type=allure.attachment_type.PNG)

    print("Step 7: Renaming the list view...")
    rename_list_view_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@title=\'Rename List View\']"))
    )
    driver.execute_script("arguments[0].click();", rename_list_view_btn)
    time.sleep(5)
    renamed_name = f"Automation by Mani {random.randint(1000, 9999)}"
    print(f"  Renamed List View Name: {renamed_name}")
    rename_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='enter-list-view-name']"))
    )
    rename_input.clear()
    rename_input.send_keys(renamed_name)
    rename_confirm_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()=\'Rename\']"))
    )
    driver.execute_script("arguments[0].click();", rename_confirm_btn)
    time.sleep(6)

    with allure.step(f"After rename to: {renamed_name}"):
        allure.attach(driver.get_screenshot_as_png(), name=f'{renamed_name}_after_rename.png', attachment_type=allure.attachment_type.PNG)

    print("  Checking if rename was successful...")
    renamed_header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']"))
    ).text.strip()
    renamed_base = re.split(r'\s*\(', renamed_header, 1)[0].strip()
    assert renamed_base == renamed_name

    print("Step 8: Asserting columns/texts are unchanged after rename...")
    after_cols = [el.text.strip() for el in driver.find_elements(By.XPATH, "//div[@class='slds-truncate']")]
    assert initial_cols == after_cols

    print("Step 9: Deleting the list view and confirming deletion...")
    delete_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//svg[@data-key='delete'] or contains(@title,'Delete') or .//span[contains(normalize-space(.),'Delete')]]"))
    )
    driver.execute_script("arguments[0].click();", delete_btn)
    confirm_delete_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[contains(text(),\'Delete\')])"))
    )
    driver.execute_script("arguments[0].click();", confirm_delete_btn)
    time.sleep(12)

    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']")))

    print("Step 10: Checking that the deleted list view is gone from the dropdown...")
    select_list_view_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@title='Select a List View']"))
    )
    driver.execute_script("arguments[0].click();", select_list_view_btn)
    time.sleep(2)
    views_after_delete = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@role='main']//li//a[1]"))
    )
    names_after = [el.text.strip() for el in views_after_delete]
    assert renamed_base not in names_after
    print("Test completed successfully. The deleted list view does not appear in the dropdown.")

