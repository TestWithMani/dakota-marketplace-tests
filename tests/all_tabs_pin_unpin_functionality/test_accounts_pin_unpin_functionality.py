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
@pytest.mark.accounts
@pytest.mark.pin_unpin
@pytest.mark.fa_portal
@pytest.mark.ria_portal
@pytest.mark.fo_portal
@pytest.mark.benchmark_portal
@pytest.mark.recommends_portal
@pytest.mark.fa_ria_portal


def test_accounts_pin_unpin_functionality(driver, base_url, credentials):
    """
    End-to-end test for Accounts tab pin/unpin functionality:
        - Login
        - Navigate to the Accounts tab
        - Check whether unpin is required and perform it if available
        - Store original header
        - Create new list view
        - Pin the new list view
        - Refresh and verify the new list appears
        - Unpin the list and refresh again
        - Verify the original header appears after unpin
        - Delete the list view
        - Include Allure screenshots for all key steps
    """
    wait = WebDriverWait(driver, 20)

    print("Step 1: Logging in...")
    username, password = credentials
    login_page = LoginPage(driver)
    login_page.navigate_to_login(base_url)
    login_page.login(username, password)

    print("Step 2: Navigating to Accounts tab...")
    driver.get(get_url(base_url, URLs.ACCOUNTS_DEFAULT))

    # Wait for the "Dakota Marketplace" row to be clickable before proceeding
    marketplace_link_xpath = "//tr[@class='slds-line-height_reset']"
    print("Waiting for 'Dakota Marketplace' row to be clickable...")
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, marketplace_link_xpath))
    )
    print("'Dakota Marketplace' row is clickable.")

    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']")))

    print("Step 3: Checking whether Unpin is needed and clicking it if available...")
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
        print("  Unpin not required, or the button was not found.")

    # Wait for the "Dakota Marketplace" row to be clickable before proceeding
    marketplace_link_xpath = "//tr[@class='slds-line-height_reset']"
    print("Waiting for 'Dakota Marketplace' row to be clickable...")
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, marketplace_link_xpath))
    )
    print("'Dakota Marketplace' row is clickable.")

    print("Step 4: Capturing original header...")
    original_header = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']"))
    ).text.strip()
    original_base = re.split(r'\s*\(', original_header, 1)[0].strip()
    print(f"  Original header: {original_header}")
    print(f"  Original base: {original_base}")
    time.sleep(2)

    print("Screenshot: Before creating a new list view")
    with allure.step("Before creating a new Accounts list view"):
        allure.attach(driver.get_screenshot_as_png(), attachment_type=allure.attachment_type.PNG)

    print("Step 5: Creating a new list view...")
    save_as_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space(.)='Save As'])[1]"))
    )
    driver.execute_script("arguments[0].click();", save_as_btn)
    time.sleep(4)
    new_list_view_name = f"Automation by Mani {random.randint(1000, 9999)}"
    print(f"  New List View Name: {new_list_view_name}")

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

    # Wait for the "Dakota Marketplace" row to be clickable before proceeding
    marketplace_link_xpath = "//tr[@class='slds-line-height_reset']"
    print("Waiting for 'Dakota Marketplace' row to be clickable...")
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, marketplace_link_xpath))
    )
    print("'Dakota Marketplace' row is clickable.")

    print("  Checking whether the new list view loads with the correct name...")
    saved_header = WebDriverWait(driver, 12).until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']"))
    ).text.strip()
    saved_base = re.split(r'\s*\(', saved_header, 1)[0].strip()
    assert saved_base == new_list_view_name, f"Expected {new_list_view_name}, but got {saved_base}"
    print(f"  New list view created successfully: {saved_base}")

    with allure.step(f"After creating new list view: {new_list_view_name}"):
        allure.attach(driver.get_screenshot_as_png(), name=f'{new_list_view_name}_after_create.png', attachment_type=allure.attachment_type.PNG)

    print("Step 6: Pinning the new list view...")
    pin_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@title='Pin this List View']"))
    )
    driver.execute_script("arguments[0].click();", pin_btn)
    time.sleep(4)
    print("  List view pinned successfully.")

    with allure.step(f"After pinning list view: {new_list_view_name}"):
        allure.attach(driver.get_screenshot_as_png(), name=f'{new_list_view_name}_after_pin.png', attachment_type=allure.attachment_type.PNG)

    print("Step 7: Refreshing page and verifying the pinned list view appears...")
    driver.refresh()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']")))

    # Wait for the "Dakota Marketplace" row to be clickable before proceeding
    marketplace_link_xpath = "//tr[@class='slds-line-height_reset']"
    print("Waiting for 'Dakota Marketplace' row to be clickable...")
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, marketplace_link_xpath))
    )
    print("'Dakota Marketplace' row is clickable.")

    refreshed_header = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']"))
    ).text.strip()
    refreshed_base = re.split(r'\s*\(', refreshed_header, 1)[0].strip()
    assert refreshed_base == new_list_view_name, f"After refresh, expected pinned list view '{new_list_view_name}', but got '{refreshed_base}'"
    print(f"  Verified: Pinned list view '{refreshed_base}' appears after refresh.")

    with allure.step(f"After refresh - pinned list view appears: {refreshed_base}"):
        allure.attach(driver.get_screenshot_as_png(), name=f'{refreshed_base}_after_refresh_pinned.png', attachment_type=allure.attachment_type.PNG)

    print("Step 8: Unpinning the list view and refreshing again...")
    unpin_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@title='Unpin this List View']"))
    )
    driver.execute_script("arguments[0].click();", unpin_btn)
    time.sleep(4)
    print("  List view unpinned successfully.")

    with allure.step(f"After unpinning list view: {new_list_view_name}"):
        allure.attach(driver.get_screenshot_as_png(), name=f'{new_list_view_name}_after_unpin.png', attachment_type=allure.attachment_type.PNG)

    driver.refresh()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']")))

    # Wait for the "Dakota Marketplace" row to be clickable before proceeding
    marketplace_link_xpath = "//tr[@class='slds-line-height_reset']"
    print("Waiting for 'Dakota Marketplace' row to be clickable...")
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, marketplace_link_xpath))
    )
    print("'Dakota Marketplace' row is clickable.")

    with allure.step(f"After unpin and refresh"):
        allure.attach(driver.get_screenshot_as_png(), name=f'after_unpin_refresh.png', attachment_type=allure.attachment_type.PNG)
    time.sleep(10)

    print("Step 9: Verifying the original header appears after unpin...")
    after_unpin_header = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']"))
    ).text.strip()
    after_unpin_base = re.split(r'\s*\(', after_unpin_header, 1)[0].strip()
    assert after_unpin_base == original_base, f"After unpin and refresh, expected original header '{original_base}', but got '{after_unpin_base}'"
    print(f"  Verified: Original header '{after_unpin_base}' shows after unpin and refresh.")

    with allure.step(f"Original header restored: {after_unpin_base}"):
        allure.attach(driver.get_screenshot_as_png(), name=f'{after_unpin_base}_original_restored.png', attachment_type=allure.attachment_type.PNG)

    print("Step 10: Deleting the created list view...")
    # Navigate to the created list view first by selecting it from the dropdown
    select_list_view_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@title='Select a List View']"))
    )
    driver.execute_script("arguments[0].click();", select_list_view_btn)
    time.sleep(3)

    # Find and click the created list view
    views_list = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@role='main']//li//a[1]"))
    )
    list_view_found = False
    for view in views_list:
        if view.text.strip() == new_list_view_name:
            driver.execute_script("arguments[0].click();", view)
            list_view_found = True
            break

    if not list_view_found:
        # Close the dropdown if the list view is not found
        driver.execute_script("arguments[0].click();", select_list_view_btn)
        raise Exception(f"Created list view '{new_list_view_name}' not found in dropdown")

    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']")))

    # Delete the list view
    delete_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//svg[@data-key='delete'] or contains(@title,'Delete') or .//span[contains(normalize-space(.),'Delete')]]"))
    )
    driver.execute_script("arguments[0].click();", delete_btn)
    confirm_delete_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[contains(text(),'Delete')])"))
    )
    driver.execute_script("arguments[0].click();", confirm_delete_btn)
    time.sleep(12)

    # Wait for the "Dakota Marketplace" row to be clickable before proceeding
    marketplace_link_xpath = "//tr[@class='slds-line-height_reset']"
    print("Waiting for 'Dakota Marketplace' row to be clickable...")
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, marketplace_link_xpath))
    )
    print("'Dakota Marketplace' row is clickable.")

    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']")))

    print("  Verifying that the deleted list view is removed from the dropdown...")
    select_list_view_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@title='Select a List View']"))
    )
    driver.execute_script("arguments[0].click();", select_list_view_btn)
    time.sleep(2)
    views_after_delete = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@role='main']//li//a[1]"))
    )
    names_after = [el.text.strip() for el in views_after_delete]
    assert new_list_view_name not in names_after, f"List view '{new_list_view_name}' still appears in dropdown after deletion"
    print(f"  Verified: List view '{new_list_view_name}' successfully deleted and removed from dropdown.")

    with allure.step(f"After deletion - list view removed: {new_list_view_name}"):
        allure.attach(driver.get_screenshot_as_png(), name=f'after_delete_verification.png', attachment_type=allure.attachment_type.PNG)

    print("Test completed successfully. Pin/unpin functionality verified for the Accounts tab.")

