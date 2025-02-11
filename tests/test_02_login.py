# ---------------------------------------------------------------------------------------------------------- #
import pytest
from pages.home_page import HomePage          # "HomePage" is a class with all the locators and funcs
from pages.login_page import LoginPage
# ---------------------------------------------------------------------------------------------------------- #
from utils.logger import logger
from utils.general_utils import generate_random_email
from utils.general_utils import capture_screenshot
from utils import read_config_data as DATA
# ---------------------------------------------------------------------------------------------------------- #
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
# ---------------------------------------------------------------------------------------------------------- #
# conftest is imported seamlessly by pytest
import time
import requests


# @pytest.mark.skip
def test_correct_login(driver, wait, request, test_context):
    try:
        home_page_obj = HomePage(driver, wait)
        login_page_obj = LoginPage(driver, wait)
        logger.info(f"[{test_context}] Init page objects for the test case")
        driver.get(DATA.get_home_url())
        logger.info(f"[{test_context}] loaded page url")

        home_page_obj.click_my_account()
        home_page_obj.click_login()

        # get valid login credentials from config.ini
        email_txt = DATA.get_email()
        password_txt = DATA.get_password()

        login_page_obj.send_email(email_txt)
        logger.info(f"[{test_context}] typed email: {email_txt}")
        login_page_obj.send_password(password_txt)
        logger.info(f"[{test_context}] typed password: {password_txt}")

        login_page_obj.click_login()
        assert login_page_obj.is_my_account_page_exists()

    except Exception as e:
        capture_screenshot(driver, request)
        logger.error(f"[{test_context}] test failed: {e}")
        pytest.fail(f"Test failed due to: {e}")


# @pytest.mark.skip
def test_invalid_login(driver, wait, request, test_context):
    try:
        home_page_obj = HomePage(driver, wait)
        login_page_obj = LoginPage(driver, wait)
        logger.info(f"[{test_context}] Init page objects for the test case")
        driver.get(DATA.get_home_url())
        logger.info(f"[{test_context}] loaded page url")

        home_page_obj.click_my_account()
        home_page_obj.click_login()

        email_txt = "myfakemail450@fakemail.com"
        password_txt = "F@K@P@$$WROD_0971"
        login_page_obj.send_email(email_txt)
        logger.info(f"[{test_context}] typed email: {email_txt}")
        login_page_obj.send_password(password_txt)
        logger.info(f"[{test_context}] typed password: {password_txt}")
        login_page_obj.click_login()

        expected_alert = "Warning: No match for E-Mail Address and/or Password"
        actual_alert = login_page_obj.get_no_such_account_alert()
        logger.info(f"[{test_context}] get_no_such_account_alert returned: {actual_alert}")
        assert expected_alert in actual_alert

    except Exception as e:
        capture_screenshot(driver, request)
        logger.error(f"[{test_context}] test failed: {e}")
        pytest.fail(f"Test failed due to: {e}")

