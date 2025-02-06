from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys


class LoginPage:
    textbox_signup_name_xpath = "//input[@placeholder='Name']"
    textbox_signup_mail_xpath = "input[data-qa='signup-email']"
    btn_signup_xpath = "//button[normalize-space()='Signup']"
    textbox_login_password_xpath = "//input[@placeholder='Password']"
    textbox_login_mail_xpath = "//input[@data-qa='login-email']"
    btn_login_xpath = "//button[normalize-space()='Login']"
    txt_error_message_xpath = "//p[normalize-space()='Your email or password is incorrect!']"

    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver  # build the obj with driver obj from the test case
        self.wait = wait

    def is_error_credentials(self, error_txt: str) -> bool:
        locator_tup = (By.XPATH, self.txt_error_message_xpath)
        return self.wait.until(EC.text_to_be_present_in_element(locator_tup, error_txt))

    def click_login(self):
        locator_tup = (By.XPATH, self.btn_login_xpath)
        self.wait.until(EC.element_to_be_clickable(locator_tup)).click()

    def send_login_password(self, password: str):
        locator_tup = (By.XPATH, self.textbox_login_password_xpath)
        textbox_username = self.wait.until(EC.visibility_of_element_located(locator_tup))
        textbox_username.clear()
        textbox_username.send_keys(password)

    def send_login_email(self, email: str):
        locator_tup = (By.XPATH, self.textbox_login_mail_xpath)
        textbox_username = self.wait.until(EC.visibility_of_element_located(locator_tup))
        textbox_username.clear()
        textbox_username.send_keys(email)

    def send_signup_username(self, username: str):
        locator_tup = (By.XPATH, self.textbox_signup_name_xpath)
        textbox_username = self.wait.until(EC.visibility_of_element_located(locator_tup))
        textbox_username.clear()
        textbox_username.send_keys(username)

    def send_signup_email(self, email: str):
        locator_tup = (By.XPATH, self.textbox_signup_mail_xpath)
        textbox_mail = self.wait.until(EC.visibility_of_element_located(locator_tup))
        textbox_mail.clear()
        textbox_mail.send_keys(email)

    def click_signup(self):
        locator_tup = (By.XPATH, self.btn_signup_xpath)
        self.wait.until(EC.element_to_be_clickable(locator_tup)).click()
