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
@pytest.mark.dakota_city_guides
@pytest.mark.list_view_crud
@pytest.mark.fa_portal
@pytest.mark.ria_portal
@pytest.mark.fo_portal
@pytest.mark.benchmark_portal
@pytest.mark.recommends_portal
@pytest.mark.fa_ria_portal


def test_dakota_city_guides_list_view_crud(driver, base_url, credentials):
    """
    End-to-end test for the Dakota City Guides tab list view:
        - Unpin if required
        - Use Save As to create a new list view
        - Rename list view
        - Delete list view
        - Verify deletion
        - Include Allure screenshots for key steps
    """
    wait = WebDriverWait(driver, 20)

    print("Step 1: Logging in...")
    username, password = credentials
    login_page = LoginPage(driver)
    login_page.navigate_to_login(base_url)
    login_page.login(username, password)

    print("Step 2: Navigating to Dakota City Guides tab...")
    driver.get(get_url(base_url, URLs.DAKOTA_CITY_GUIDES))

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

    print("Step 4: Capturing the original header/base text...")
    original_header = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']"))
    ).text.strip()
    original_base = re.split(r'\s*\(', original_header, 1)[0].strip()
    time.sleep(1)

    print("Step 5: Collecting original column texts...")
    initial_cols = [el.text.strip() for el in driver.find_elements(By.XPATH, "//div[@class='slds-truncate']")]

    print("Screenshot: Before saving a list view")
    with allure.step("Before saving new Dakota City Guides list view"):
        allure.attach(driver.get_screenshot_as_png(), attachment_type=allure.attachment_type.PNG)

    print("Step 6: Performing 'Save As' to create a new list view...")
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

    # Wait for the "Dakota Marketplace" row to be clickable before proceeding
    marketplace_link_xpath = "//tr[@class='slds-line-height_reset']"
    print("Waiting for 'Dakota Marketplace' row to be clickable...")
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, marketplace_link_xpath))
    )
    print("'Dakota Marketplace' row is clickable.")

    with allure.step(f"After rename to: {renamed_name}"):
        allure.attach(driver.get_screenshot_as_png(), name=f'{renamed_name}_after_rename.png', attachment_type=allure.attachment_type.PNG)

    print("  Checking whether the rename was successful...")
    renamed_header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='headerTitle']"))
    ).text.strip()
    renamed_base = re.split(r'\s*\(', renamed_header, 1)[0].strip()
    assert renamed_base == renamed_name

    print("Step 8: Deleting the list view and confirming the deletion...")
    delete_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//svg[@data-key='delete'] or contains(@title,'Delete') or .//span[contains(normalize-space(.),'Delete')]]"))
    )
    driver.execute_script("arguments[0].click();", delete_btn)
    confirm_delete_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[contains(text(),\'Delete\')])"))
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

    print("Step 9: Checking that the deleted list view is removed from the dropdown...")
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
    print("Test completed successfully. The deleted list view no longer appears in the dropdown.")

