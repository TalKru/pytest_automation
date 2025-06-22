
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys
from utils.logger import logger


class LoginPage:
    # url = "https://naveenautomationlabs.com/opencart/index.php?route=account/login"
    textbox_email = (By.XPATH, "//input[@id='input-email']")
    textbox_password = (By.XPATH, "//input[@id='input-password']")
    btn_login = (By.XPATH, "//input[@value='Login']")
    btn_forgot_password = (By.XPATH, "//a[text()='Forgotten Password']")
    btn_continue = (By.XPATH, "//a[normalize-space()='Continue']")
    text_my_account = (By.XPATH, "//h2[normalize-space()='My Account']")
    text_no_such_account = (By.XPATH, "//div[@class='alert alert-danger alert-dismissible']")

    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver  # build the obj with driver obj from the test case
        self.wait = wait

    def send_email(self, mail: str):
        textbox = self.wait.until(EC.visibility_of_element_located(self.textbox_email))
        textbox.clear()
        textbox.send_keys(mail)

    def send_password(self, password: str):
        textbox = self.wait.until(EC.visibility_of_element_located(self.textbox_password))
        textbox.clear()
        textbox.send_keys(password)

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.btn_login))
        login_btn.click()

    def click_forgot_password(self):
        forgot_password_btn = self.wait.until(EC.element_to_be_clickable(self.btn_forgot_password))
        forgot_password_btn.click()

    def click_continue(self):
        continue_btn = self.wait.until(EC.element_to_be_clickable(self.btn_continue))
        continue_btn.click()

    def get_no_such_account_alert(self) -> str:
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.text_no_such_account))
            return element.text

        except Exception as e:
            # print(f"Failed to get no_such_account_text: {e}")
            logger.error(f"[get_no_such_account_alert]: Failed to get no_such_account_text: {e}")
            return ""

    def is_my_account_page_exists(self) -> bool:
        try:
            element = self.driver.find_element(*self.text_my_account)  # note the '*' syntax for tuple unpacking
            return element.is_displayed()

        except Exception as e:
            # print(f"Failed to get confirmation_login_text: {e}")
            logger.error(f"[is_my_account_page_exists]: Failed to get confirmation_login_text: {e}")
            return False

