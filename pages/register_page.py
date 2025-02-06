from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys


class RegisterPage:
    # locators - OF A SINGLE PAGE
    # url = "https://naveenautomationlabs.com/opencart/index.php?route=account/register"
    textbox_firstname_xpath = "//input[@id='input-firstname']"
    textbox_lastname_xpath = "//input[@id='input-lastname']"
    textbox_email_xpath = "//input[@id='input-email']"
    textbox_telephone_xpath = "//input[@id='input-telephone']"
    textbox_password_xpath = "//input[@id='input-password']"
    textbox_confirm_password_xpath = "//input[@id='input-confirm']"

    radio_subscribe_yes_xpath = "//input[@type='radio' and @name='newsletter' and @value='1']"
    radio_subscribe_no_xpath = "//input[@type='radio' and @name='newsletter' and @value='0']"
    checkbox_agree_xpath = "//input[@type='checkbox' and @name='agree' and @value='1']"

    btn_continue_xpath = "//input[@value='Continue']"

    text_msg_conf_xpath = "//h1[normalize-space()='Your Account Has Been Created!']"

    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver  # build the obj with driver obj from the test case
        self.wait = wait

    def send_firstname(self, firstname: str):
        tup = (By.XPATH, self.textbox_firstname_xpath)
        txtbox = self.wait.until(EC.visibility_of_element_located(tup))
        txtbox.clear()
        txtbox.send_keys(firstname)

    def send_lastname(self, lastname: str):
        tup = (By.XPATH, self.textbox_lastname_xpath)
        txtbox = self.wait.until(EC.visibility_of_element_located(tup))
        txtbox.clear()
        txtbox.send_keys(lastname)

    def send_email(self, mail: str):
        tup = (By.XPATH, self.textbox_email_xpath)
        txtbox = self.wait.until(EC.visibility_of_element_located(tup))
        txtbox.clear()
        txtbox.send_keys(mail)

    def send_telephone(self, telephone: str):
        tup = (By.XPATH, self.textbox_telephone_xpath)
        txtbox = self.wait.until(EC.visibility_of_element_located(tup))
        txtbox.clear()
        txtbox.send_keys(telephone)

    def send_password(self, password: str):
        tup = (By.XPATH, self.textbox_password_xpath)
        txtbox = self.wait.until(EC.visibility_of_element_located(tup))
        txtbox.clear()
        txtbox.send_keys(password)

    def send_password_confirm(self, password_confirm: str):
        tup = (By.XPATH, self.textbox_confirm_password_xpath)
        txtbox = self.wait.until(EC.visibility_of_element_located(tup))
        txtbox.clear()
        txtbox.send_keys(password_confirm)

    def click_no_subscribe(self):
        tup = (By.XPATH, self.radio_subscribe_no_xpath)
        self.wait.until(EC.element_to_be_clickable(tup)).click()

    def click_yes_subscribe(self):
        tup = (By.XPATH, self.radio_subscribe_yes_xpath)
        self.wait.until(EC.element_to_be_clickable(tup)).click()

    def click_agree_terms(self):
        tup = (By.XPATH, self.checkbox_agree_xpath)
        self.wait.until(EC.element_to_be_clickable(tup)).click()

    def click_continue(self):
        tup = (By.XPATH, self.btn_continue_xpath)
        self.wait.until(EC.element_to_be_clickable(tup)).click()

    def get_confirm_account_msg(self):
        tup = (By.XPATH, self.text_msg_conf_xpath)
        try:
            element = self.wait.until(EC.visibility_of_element_located(tup))
            return element.text

        except Exception as e:
            print(f"Failed to get confirm account msg: {e}")
            return None


