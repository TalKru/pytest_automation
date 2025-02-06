import pytest
from pages.home_page import HomePage          # "HomePage" is a class with all the locators and funcs
from pages.register_page import RegisterPage  # "RegisterPage" is a class with all the locators and funcs
from utils.general_utils import generate_random_email, capture_screenshot
# ---------------------------------------------------------------------------------------------------------- #
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
# ---------------------------------------------------------------------------------------------------------- #
# conftest is imported seamlessly by pytest
import time


BASE_URL = "https://naveenautomationlabs.com/opencart/"


@pytest.mark.repeat(3)  # will run the same test 3 times
def test_correct_account_registration(driver: webdriver, wait: WebDriverWait):
    # init imported page objects with driver and wait from conftest
    home_page_obj = HomePage(driver, wait)
    register_page_obj = RegisterPage(driver, wait)

    driver.get(BASE_URL)
    home_page_obj.click_my_account()
    home_page_obj.click_register()

    register_page_obj.send_firstname("Richard")
    register_page_obj.send_lastname("Fox")

    rand_email = generate_random_email()  # random mail generator
    register_page_obj.send_email(rand_email)
    register_page_obj.send_telephone("012777333")
    register_page_obj.send_password("pass12345")
    register_page_obj.send_password_confirm("pass12345")

    register_page_obj.click_no_subscribe()
    register_page_obj.click_agree_terms()
    register_page_obj.click_continue()

    expected_msg = "Your Account Has Been Created!"
    actual_msg = register_page_obj.get_confirm_account_msg()

    assert expected_msg in actual_msg


def test_missing_agreement_checkbox_error_msg(driver: webdriver, wait: WebDriverWait):
    home_page_obj = HomePage(driver, wait)
    register_page_obj = RegisterPage(driver, wait)

    driver.get(BASE_URL)
    home_page_obj.click_my_account()
    home_page_obj.click_register()

    register_page_obj.send_firstname("Richard")
    register_page_obj.send_lastname("Fox")

    rand_email = generate_random_email()
    register_page_obj.send_email(rand_email)
    register_page_obj.send_telephone("012777333")
    register_page_obj.send_password("pass12345")
    register_page_obj.send_password_confirm("pass12345")

    register_page_obj.click_no_subscribe()
    register_page_obj.click_continue()

    actual_msg = register_page_obj.get_error_missing_checkbox_agree_policy()
    expected_error_msg = "Warning: You must agree to the Privacy Policy!"

    assert expected_error_msg in actual_msg


def test_passwords_mismatch_on_registration(driver: webdriver, wait: WebDriverWait):
    home_page_obj = HomePage(driver, wait)
    register_page_obj = RegisterPage(driver, wait)

    driver.get(BASE_URL)
    home_page_obj.click_my_account()
    home_page_obj.click_register()

    register_page_obj.send_firstname("Richard")
    register_page_obj.send_lastname("Fox")

    rand_email = generate_random_email()
    register_page_obj.send_email(rand_email)
    register_page_obj.send_telephone("012777333")
    register_page_obj.send_password("pass#12345")          # pass#12345
    register_page_obj.send_password_confirm("pass#00000")  # pass#00000

    register_page_obj.click_no_subscribe()
    register_page_obj.click_continue()

    actual_msg = register_page_obj.get_error_passwords_mismatch()
    expected_error_msg = "Password confirmation does not match password!"

    assert expected_error_msg in actual_msg





