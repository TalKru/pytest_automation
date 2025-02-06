
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys


class LoginPage:
    # locators - OF A SINGLE PAGE
    # url = "https://naveenautomationlabs.com/opencart/index.php?route=account/login"
    textbox_email_xpath = "//input[@id='input-email']"
    textbox_password_xpath = "//input[@id='input-password']"
    btn_login_xpath = "//input[@value='Login']"

    # constructor
    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver  # build the obj with driver obj from the test case
        self.wait = wait

    def send_email(self, mail: str):
        tup = (By.XPATH, self.textbox_email_xpath)
        txtbox = self.wait.until(EC.visibility_of_element_located(tup))
        txtbox.clear()
        txtbox.send_keys(mail)

    def send_password(self, password: str):
        tup = (By.XPATH, self.textbox_password_xpath)
        txtbox = self.wait.until(EC.visibility_of_element_located(tup))
        txtbox.clear()
        txtbox.send_keys(password)

    def click_login(self):
        tup = (By.XPATH, self.btn_login_xpath)
        login_btn = self.wait.until(EC.element_to_be_clickable(tup))
        login_btn.click()







