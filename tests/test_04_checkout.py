# ---------------------------------------------------------------------------------------------------------- #
import pytest

from pages.home_page import HomePage          # "HomePage" is a class with all the locators and funcs
from pages.checkout_page import CheckoutPage
# ---------------------------------------------------------------------------------------------------------- #
from utils.logger import logger
from utils.general_utils import generate_random_email
from utils.general_utils import capture_screenshot
from utils import read_config_data as DATA
# ---------------------------------------------------------------------------------------------------------- #
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
# ---------------------------------------------------------------------------------------------------------- #
# conftest is imported seamlessly by pytest
import time
import requests


def test_currency_options(driver, wait, request, test_context):
    """
        Test Case: check if all currency options are available
        1. click currency selector
        2. pull list of all currency options as strings
        3. loop on each option
        4. verify each option is defined in the setup list
        Expected Result:
        - currency should contain exactly 3 different types:
          £ Pound Sterling
          € Euro
          $ US Dollar
        """
    try:
        home_page_obj = HomePage(driver, wait)
        checkout_page_obj = CheckoutPage(driver, wait)

        logger.info(f"[{test_context}] Init page objects for the test case")
        driver.get(DATA.get_home_url())
        logger.info(f"[{test_context}] loaded page url")

        home_page_obj.click_checkout()
        logger.info(f"[{test_context}] navigate to checkout page")

        checkout_page_obj.click_currency_btn()
        logger.info(f"[{test_context}] click_currency_btn")

        currency_list = checkout_page_obj.get_list_of_currency_options()
        currency_symbols = ('€', '£', '$')

        logger.info(f"[{test_context}] loop on every currency option and verify it's in the list")
        for option in currency_list:
            currency_symbol = option.split()[0]

            assert currency_symbol in currency_symbols

    except Exception as e:
        capture_screenshot(driver, request)
        logger.error(f"[{test_context}] test failed: {e}")
        pytest.fail(f"Test failed due to: {e}")


