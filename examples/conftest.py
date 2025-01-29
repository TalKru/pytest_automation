
# ---------------------------------------------------------------------
# locator_tuple = (By.ID, 'start-date')
# element = wait.until(EC.element_to_be_clickable(locator_tuple))
# ActionChains(driver).move_to_element(element).click().perform()
# ---------------------------------------------------------------------
# element = driver.find_element(By.ID, 'start-date')
# element.click()
# ---------------------------------------------------------------------

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys
import time


@pytest.fixture(scope="function")
def driver() -> webdriver:

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--incognito")  # will mess up file downloads
    # chrome_options.add_argument("--headless=new")
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def wait(driver, wait_time_sec=10) -> WebDriverWait:
    wait = WebDriverWait(driver, wait_time_sec, poll_frequency=1, ignored_exceptions=[])
    # driver.implicitly_wait(WAIT_TIME_SEC)
    return wait



