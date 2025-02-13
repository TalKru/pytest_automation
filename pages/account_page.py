
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys


class AccountPage:
    # locators - OF A SINGLE PAGE
    btn_dropdown_account_xpath = "//a[@title='My Account']"
    btn_logout_xpath = "//a[@class='list-group-item'][normalize-space()='Logout']"

    text_logout_msg_xpath = "//*[@id='content']/p[1]"

    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver  # build the obj with driver obj from the test case
        self.wait = wait

    def click_logout(self):
        tup = (By.XPATH, self.btn_logout_xpath)
        logout_btn = self.wait.until(EC.element_to_be_clickable(tup))
        logout_btn.click()

    def get_logout_text(self):
        tup = (By.XPATH, self.text_logout_msg_xpath)
        return self.wait.until(EC.element_to_be_clickable(tup)).text


