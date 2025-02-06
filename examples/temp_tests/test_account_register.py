import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from utils.general_utils import capture_screenshot
import time
from datetime import datetime
# ------------------------------------------------------------------ #
from utils.general_utils import capture_screenshot
# ------------------------------------------------------------------ #
from pages import home_page, login_page, signup_page
# ------------------------------------------------------------------ #


def test_wrong_login(driver: webdriver, wait: WebDriverWait):

    driver.get('https://www.automationexercise.com/')

    home_page_obj = home_page.HomePage(driver, wait)
    home_page_obj.click_register()

    login_page_obj = login_page.LoginPage(driver, wait)
    login_page_obj.send_login_email('wrong@email.com')
    login_page_obj.send_login_password('pass123')
    login_page_obj.click_login()

    is_error_msg = login_page_obj.is_error_credentials("Your email or password is incorrect!")

    assert is_error_msg, 'error message (for wrong login) not found'






