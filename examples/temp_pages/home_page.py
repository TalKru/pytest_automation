from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys


class HomePage:
    # url = "https://www.automationexercise.com/"
    login_xpath = "//a[normalize-space()='Signup / Login']"
    products_xpath = "//a[@href='/products']"
    cart_xpath = "//a[@href='/view_cart']"

    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver  # build the obj with driver obj from the test case
        self.wait = wait

    def click_register(self):
        locator_tup = (By.XPATH, self.login_xpath)
        register_element = self.wait.until(EC.presence_of_element_located(locator_tup))
        register_element.click()
