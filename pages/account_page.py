
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys


class AccountPage:

    btn_dropdown_account = (By.XPATH, "//a[@title='My Account']")
    btn_logout = (By.XPATH, "//a[@class='list-group-item'][normalize-space()='Logout']")
    text_logout_msg = (By.XPATH, "//*[@id='content']/p[1]")

    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver  # build the obj with driver obj from the test case
        self.wait = wait

    def click_logout(self):
        logout_btn = self.wait.until(EC.element_to_be_clickable(*self.btn_logout))
        logout_btn.click()

    def get_logout_text(self):
        return self.wait.until(EC.element_to_be_clickable(*self.text_logout_msg)).text


