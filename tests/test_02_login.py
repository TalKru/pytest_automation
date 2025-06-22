# ---------------------------------------------------------------------------------------------------------- #
import pytest
from pages.home_page import HomePage          # "HomePage" is a class with all the locators and funcs
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from pages.register_page import RegisterPage
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


# @pytest.mark.skip
@pytest.mark.sanity
@pytest.mark.smoke
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
        logger.info(f"[{test_context}] clicked login...")
        assert login_page_obj.is_my_account_page_exists()

    except Exception as e:
        capture_screenshot(driver, request)
        logger.error(f"[{test_context}] test failed: {e}")
        pytest.fail(f"Test failed due to: {e}")


# @pytest.mark.skip
@pytest.mark.regression
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
        password_txt = "F@KePa$$WoRD_0971"
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


# @pytest.mark.skip
@pytest.mark.sanity
def test_correct_logout(driver, wait, request, test_context):
    try:
        home_page_obj = HomePage(driver, wait)
        login_page_obj = LoginPage(driver, wait)
        logout_page_obj = AccountPage(driver, wait)
        logger.info(f"[{test_context}] Init page objects for the test case")
        driver.get(DATA.get_home_url())
        logger.info(f"[{test_context}] loaded page url")

        home_page_obj.click_my_account()
        home_page_obj.click_login()
        email_txt = DATA.get_email()        # get valid login credentials from config.ini
        password_txt = DATA.get_password()  # get valid login credentials from config.ini
        login_page_obj.send_email(email_txt)
        logger.info(f"[{test_context}] typed email: {email_txt}")
        login_page_obj.send_password(password_txt)
        logger.info(f"[{test_context}] typed password: {password_txt}")
        login_page_obj.click_login()
        logger.info(f"[{test_context}] account logged in...")

        logout_page_obj.click_logout()
        logger.info(f"[{test_context}] account logged out...")

        expected_txt = "You have been logged off your account"
        logout_text = logout_page_obj.get_logout_text()
        logger.info(f"[{test_context}] {logout_text=}")
        assert expected_txt in logout_text

    except Exception as e:
        capture_screenshot(driver, request)
        logger.error(f"[{test_context}] test failed: {e}")
        pytest.fail(f"Test failed due to: {e}")


@pytest.mark.sanity
def test_continue_to_registration(driver, wait, request, test_context):
    try:
        home_page_obj = HomePage(driver, wait)
        login_page_obj = LoginPage(driver, wait)
        register_page_obj = RegisterPage(driver, wait)
        logger.info(f"[{test_context}] Init page objects for the test case")
        driver.get(DATA.get_home_url())
        logger.info(f"[{test_context}] loaded page url")

        home_page_obj.click_my_account()
        logger.info(f"[{test_context}] clicked my account")
        home_page_obj.click_login()
        logger.info(f"[{test_context}] clicked login")
        login_page_obj.click_continue()
        logger.info(f"[{test_context}] clicked my continue")

        expected_text = "Register Account"
        register_text = register_page_obj.get_register_account_text()
        logger.info(f"[{test_context}] {register_text=}")
        assert expected_text in register_text

    except Exception as e:
        capture_screenshot(driver, request)
        logger.error(f"[{test_context}] test failed: {e}")
        pytest.fail(f"Test failed due to: {e}")




