"""
run in terminal -->      pytest -s .\tests\test_basic.py --browser chrome --html=reports\report.html
"""
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys
from utils.general_utils import capture_screenshot
import time
from datetime import datetime


def test_login(driver: webdriver, wait: WebDriverWait, request):  # Type hints added
    """
    Even with the correct imports, PyCharm sometimes struggles with autocompletion for objects
    that are passed in as arguments (like driver and wait from the fixtures).

    Add type hints to your test function arguments.
    This tells PyCharm (and Python's type checker) what type of object driver and wait are.
           ___________      ________________
    (driver: webdriver, wait: WebDriverWait)
    """
    try:
        driver.get("https://opensource-demo.orangehrmlive.com/")

        tuple1 = (By.XPATH, "//input[@class='oxd-input oxd-input--active' and @name='username']")
        username_box = wait.until(EC.presence_of_element_located(tuple1))
        username_box.clear()
        username_box.send_keys('Admin')

        tuple2 = (By.XPATH, "//input[@class='oxd-input oxd-input--active' and @type='password' and @name='password']")
        password_box = wait.until(EC.presence_of_element_located(tuple2))
        password_box.clear()
        password_box.send_keys('admin123')

        tuple3 = (By.XPATH, "//button[@class='oxd-button oxd-button--medium oxd-button--main orangehrm-login-button'"
                            " and @type='submit']")
        login_btn = wait.until(EC.element_to_be_clickable(tuple3))
        login_btn.click()

        expected_text = "Time at Work"
        actual_text = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//p[normalize-space()='Time at Work']"))).text

        assert expected_text in actual_text, f"Expected '{expected_text}' to be in '{actual_text}'"

    except Exception as e:
        print(f"Error message: {e}")
        screenshot_path = capture_screenshot(driver, request)
        pytest.fail(f"Test failed: {e}... Screenshot saved at: {screenshot_path}")


def test_logo(driver: webdriver, request):
    try:
        driver.get("https://opensource-demo.orangehrmlive.com/")
        xpath = "//div[@class='orangehrm-login-logo']//img[@alt='orangehrm-logo']"

        time.sleep(2)

        status = driver.find_element(By.XPATH, xpath).is_displayed()
        assert status is not True

    except Exception as e:
        print(f"Error message: {e}")
        screenshot_path = capture_screenshot(driver, request)
        pytest.fail(f"Test failed: {e}... Screenshot saved at: {screenshot_path}")












