
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
    btn_forgot_password_xpath = "//a[text()='Forgotten Password']"

    text_my_account_xpath = "//h2[normalize-space()='My Account']"
    text_no_such_account_xpath = "//div[@class='alert alert-danger alert-dismissible']"

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

    def click_forgot_password(self):
        tup = (By.XPATH, self.btn_forgot_password_xpath)
        forgot_password_btn = self.wait.until(EC.element_to_be_clickable(tup))
        forgot_password_btn.click()

    def get_no_such_account_alert(self) -> str:
        tup = (By.XPATH, self.text_no_such_account_xpath)
        try:
            return self.wait.until(EC.element_to_be_clickable(tup)).text
        except Exception as e:
            print(f"Failed to get no_such_account_text: {e}")
            return ""

    def is_my_account_page_exists(self) -> bool:
        try:
            return self.driver.find_element(By.XPATH, self.text_my_account_xpath).is_displayed()
        except Exception as e:
            print(f"Failed to get confirmation_login_text: {e}")
            return False

