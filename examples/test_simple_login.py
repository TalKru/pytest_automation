from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys
import time


def test_login(driver: webdriver, wait: WebDriverWait):  # Type hints added
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

        tuple1 = (By.XPATH, "//input[@placeholder='Username']")
        username_box = wait.until(EC.presence_of_element_located(tuple1))
        username_box.clear()
        username_box.send_keys('Admin')

        tuple2 = (By.XPATH, "//input[@placeholder='Password']")
        password_box = wait.until(EC.presence_of_element_located(tuple2))
        password_box.clear()
        password_box.send_keys('admin123')

        tuple3 = (By.XPATH, "//button[normalize-space()='Login']")
        login_btn = wait.until(EC.element_to_be_clickable(tuple3))
        login_btn.click()

        expected_text = "Time at Work"
        actual_text = wait.until(EC.presence_of_element_located((By.XPATH, "//p[normalize-space()='Time at Work']"))).text
        assert expected_text in actual_text, f"Expected '{expected_text}' to be in '{actual_text}'"

    except Exception as e:
        print(f"Error message: {e}")
        timestamp = datetime.now().strftime("%Y_%m_%d-%I_%M_%S") + '.png'
        driver.save_screenshot(timestamp)
        pytest.fail(f"Test failed: {e}")







