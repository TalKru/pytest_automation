# ------------------------------------------------------------------------
import pytest
# ------------------------------------------------------------------------
import os.path
import time
# ------------------------------------------------------------------------
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys
# ------------------------------------------------------------------------
from utils import excel_utils as utils
from utils.general_utils import capture_screenshot
# ------------------------------------------------------------------------


def test_sheet_calc(driver: webdriver, wait: WebDriverWait, request):
    try:
        driver.get('https://www.moneycontrol.com/fixed-income/calculator/state-bank-of-india-sbi/fixed-deposit-calculator-SBI-BSB001.html')
        # NOTE: make sure the path structure is correct
        excel_file_path = os.path.abspath(r'D:\dev\pytest_automation\examples\calc-data.xlsx')

        # optional for visuals
        driver.execute_script(f"document.body.style.zoom='125%'")  # zoom in 150%
        ActionChains(driver).move_to_element(driver.find_element(By.ID, 'frequency'))

        # ---------------------------------------------------------------------------------------------------
        # in case pop-up msg opens
        elements = driver.find_elements(By.ID, 'wzrk-cancel')
        if elements:  # If the list is not empty
            wait.until(EC.element_to_be_clickable((By.ID, 'wzrk-cancel'))).click()
        # ---------------------------------------------------------------------------------------------------

        # get only the data test rows from the file
        r = utils.get_row_count(excel_file_path, 'Sheet1')
        excel_data_rows = range(2, r + 1)

        for i in excel_data_rows:
            print(f'-------------------(test row number: {i})-------------------')

            value1 = utils.read_data(excel_file_path, 'Sheet1', i, 1)  # get data from excel
            field1 = driver.find_element(By.ID, 'principal')                        # find element
            field1.clear()                                                          # clear old data
            field1.send_keys(value1)                                                # pass data to element
            # ---------------------------------------------------------------------------------------------------
            value2 = utils.read_data(excel_file_path, 'Sheet1', i, 2)
            field2 = driver.find_element(By.ID, 'interest')
            field2.clear()
            field2.send_keys(value2)
            # ---------------------------------------------------------------------------------------------------
            value3 = utils.read_data(excel_file_path, 'Sheet1', i, 3)
            field3 = driver.find_element(By.ID, 'tenure')
            field3.clear()
            field3.send_keys(value3)
            # ---------------------------------------------------------------------------------------------------
            value4 = utils.read_data(excel_file_path, 'Sheet1', i, 4)

            dropdown1 = driver.find_element(By.ID, 'tenurePeriod')
            Select(dropdown1).select_by_visible_text(value4)
            # ---------------------------------------------------------------------------------------------------
            value5 = utils.read_data(excel_file_path, 'Sheet1', i, 5)

            dropdown2 = driver.find_element(By.ID, 'frequency')
            Select(dropdown2).select_by_visible_text(value5)
            # ---------------------------------------------------------------------------------------------------
            xpath = "//img[@src='https://images.moneycontrol.com/images/mf_revamp/btn_calcutate.gif']"
            calc_btn = driver.find_element(By.XPATH, xpath)
            calc_btn.click()
            # ---------------------------------------------------------------------------------------------------
            xlsx_value = utils.read_data(excel_file_path, 'Sheet1', i, 6)
            url_value = driver.find_element(By.ID, 'resp_matval').text

            print(f'excel value: {xlsx_value}')
            print(f'web result value: {url_value}')

            if float(xlsx_value) == float(url_value):
                utils.write_to_cell(excel_file_path, 'Sheet1', i, 8, "PASS")
                utils.fill_cell_color(excel_file_path, 'Sheet1', i, 8, 'green')
                print("[v][PASS]")
            else:
                utils.write_to_cell(excel_file_path, 'Sheet1', i, 8, "FAIL")
                utils.fill_cell_color(excel_file_path, 'Sheet1', i, 8, 'red')
                print("[x][FAIL]")

            driver.find_element(By.XPATH, "//*[@id='fdMatVal']/div[2]/a[2]/img").click()  # click the CLEAR button
            time.sleep(0.5)

    except Exception as e:
        print(f"Error message: {e}")
        screenshot_path = capture_screenshot(driver, request)
        pytest.fail(f"Test failed: {e}... Screenshot saved at: {screenshot_path}")







