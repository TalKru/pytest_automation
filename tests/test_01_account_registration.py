# ---------------------------------------------------------------------------------------------------------- #
import pytest
from pages.home_page import HomePage          # "HomePage" is a class with all the locators and funcs
from pages.register_page import RegisterPage  # "RegisterPage" is a class with all the locators and funcs
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


#@pytest.mark.skip
def test_mock_fail_for_screenshot(driver, wait, request, test_context):
    try:
        logger.warning(f"[{test_context}] This test case is an example FAIL for a screenshot")
        home_page_obj = HomePage(driver, wait)
        logger.info(f"[{test_context}] Init page objects for the test case")
        driver.get(DATA.get_home_url())
        logger.info(f"[{test_context}] loaded page url")
        home_page_obj.click_my_account()
        logger.warning(f"[{test_context}] Warning! assert False")
        assert False

    except Exception as e:
        capture_screenshot(driver, request)
        logger.error(f"[{test_context}] test failed: {e}")
        pytest.fail(f"Test failed due to: {e}")


# @pytest.mark.skip
@pytest.mark.sanity
@pytest.mark.repeat(3)  # will run the same test 3 times
def test_correct_account_registration(driver, wait, request, test_context):
    try:
        # init imported page objects with driver and wait from conftest
        home_page_obj = HomePage(driver, wait)
        register_page_obj = RegisterPage(driver, wait)
        logger.info(f"[{test_context}] Init page objects for the test case")

        driver.get(DATA.get_home_url())  # read the URL from config.ini file using utils.read_config_data.py module
        logger.info(f"[{test_context}] loaded page url")

        home_page_obj.click_my_account()
        home_page_obj.click_register()

        register_page_obj.send_firstname("Richard")
        register_page_obj.send_lastname("Fox")

        rand_email = generate_random_email()  # random mail generator

        register_page_obj.send_email(rand_email)
        logger.info(f"[{test_context}] random mail used for registration: {rand_email}")

        register_page_obj.send_telephone("012777333")
        register_page_obj.send_password("pass12345")
        register_page_obj.send_password_confirm("pass12345")
        logger.info(f"[{test_context}] filled registration data")

        register_page_obj.click_no_subscribe()
        logger.info(f"[{test_context}] clicked no_subscribe")
        register_page_obj.click_agree_terms()
        logger.info(f"[{test_context}] clicked agree_terms")
        register_page_obj.click_continue()
        logger.info(f"[{test_context}] clicked continue")

        expected_msg = "Your Account Has Been Created!"
        actual_msg = register_page_obj.get_confirm_account_msg()
        logger.info(f"[{test_context}] test extracted from the success page: {actual_msg}")
        assert expected_msg in actual_msg

    except Exception as e:
        capture_screenshot(driver, request)
        logger.error(f"[{test_context}] test failed: {e}")
        pytest.fail(f"Test failed due to: {e}")


# @pytest.mark.skip
@pytest.mark.regression
@pytest.mark.repeat(1)
def test_missing_agreement_checkbox_error_msg(driver, wait, request, test_context):
    try:
        home_page_obj = HomePage(driver, wait)
        register_page_obj = RegisterPage(driver, wait)
        logger.info(f"[{test_context}] Init page objects for the test case")

        driver.get(DATA.get_home_url())
        logger.info(f"[{test_context}] loaded page url")

        home_page_obj.click_my_account()
        home_page_obj.click_register()

        register_page_obj.send_firstname("Richard")
        register_page_obj.send_lastname("Fox")

        rand_email = generate_random_email()
        register_page_obj.send_email(rand_email)
        register_page_obj.send_telephone("012777333")
        register_page_obj.send_password("pass12345")
        register_page_obj.send_password_confirm("pass12345")
        logger.info(f"[{test_context}] filled registration data")

        register_page_obj.click_no_subscribe()
        logger.info(f"[{test_context}] clicked no_subscribe")
        register_page_obj.click_continue()
        logger.info(f"[{test_context}] clicked continue")

        expected_error_msg = "Warning: You must agree to the Privacy Policy!"
        actual_msg = register_page_obj.get_error_missing_checkbox_agree_policy()
        logger.info(f"[{test_context}] got msg: {actual_msg}")

        assert expected_error_msg in actual_msg

    except Exception as e:
        capture_screenshot(driver, request)
        logger.error(f"[{test_context}] test failed: {e}")
        pytest.fail(f"Test failed due to: {e}")


# @pytest.mark.skip
@pytest.mark.regression
@pytest.mark.repeat(2)
def test_passwords_mismatch_on_registration(driver, wait, request, test_context):
    try:
        home_page_obj = HomePage(driver, wait)
        register_page_obj = RegisterPage(driver, wait)
        logger.info(f"[{test_context}] Init page objects for the test case")

        driver.get(DATA.get_home_url())
        logger.info(f"[{test_context}] loaded page url")

        home_page_obj.click_my_account()
        home_page_obj.click_register()

        register_page_obj.send_firstname("Richard")
        register_page_obj.send_lastname("Fox")

        rand_email = generate_random_email()
        register_page_obj.send_email(rand_email)
        register_page_obj.send_telephone("012777333")
        register_page_obj.send_password("pass#12345")          # pass#12345
        register_page_obj.send_password_confirm("pass#00000")  # pass#00000
        logger.info(f"[{test_context}] filled registration data")

        register_page_obj.click_no_subscribe()
        logger.info(f"[{test_context}] clicked no_subscribe")
        register_page_obj.click_continue()
        logger.info(f"[{test_context}] clicked continue")

        actual_msg = register_page_obj.get_error_passwords_mismatch()
        expected_error_msg = "Password confirmation does not match password!"
        assert expected_error_msg in actual_msg

    except Exception as e:
        capture_screenshot(driver, request)
        logger.error(f"[{test_context}] test failed: {e}")
        pytest.fail(f"Test failed due to: {e}")







