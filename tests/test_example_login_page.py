
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from utils.general_utils import capture_screenshot
import time
from datetime import datetime
from pages.example_login_page_objects import LoginPage


def test_login_page(driver: webdriver):
    driver.get('https://practicetestautomation.com/practice-test-login/')
    page = LoginPage(driver)
    page.send_username('student')
    page.send_password('Password123')
    page.click_login()

    page_title: str = driver.title
    correct_title = 'Logged In Successfully | Practice Test Automation'

    assert page_title == correct_title


