from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys
from utils.logger import logger


class RegisterPage:
    # url = "https://naveenautomationlabs.com/opencart/index.php?route=account/register"
    textbox_firstname = (By.XPATH, "//input[@id='input-firstname']")
    textbox_lastname = (By.XPATH, "//input[@id='input-lastname']")
    textbox_email = (By.XPATH, "//input[@id='input-email']")
    textbox_telephone = (By.XPATH, "//input[@id='input-telephone']")
    textbox_password = (By.XPATH, "//input[@id='input-password']")
    textbox_confirm_password = (By.XPATH, "//input[@id='input-confirm']")
    radio_yes_subscribe = (By.XPATH, "//input[@type='radio' and @name='newsletter' and @value='1']")
    radio_no_subscribe = (By.XPATH, "//input[@type='radio' and @name='newsletter' and @value='0']")
    checkbox_agree = (By.XPATH, "//input[@type='checkbox' and @name='agree' and @value='1']")
    btn_continue = (By.XPATH, "//input[@value='Continue']")
    text_register_acc = (By.XPATH, "//*[@id='content']/h1")
    text_msg_conf = (By.XPATH, "//h1[normalize-space()='Your Account Has Been Created!']")
    text_warning_not_agreed_to_policy = (By.XPATH, "//div[@class='alert alert-danger alert-dismissible']")
    text_err_passwords_mismatch = (By.XPATH, "//div[@class='text-danger']")

    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver  # build the obj with driver obj from the test case
        self.wait = wait

    def send_firstname(self, firstname: str):
        txtbox = self.wait.until(EC.visibility_of_element_located(self.textbox_firstname))
        txtbox.clear()
        txtbox.send_keys(firstname)

    def send_lastname(self, lastname: str):
        txtbox = self.wait.until(EC.visibility_of_element_located(self.textbox_lastname))
        txtbox.clear()
        txtbox.send_keys(lastname)

    def send_email(self, mail: str):
        txtbox = self.wait.until(EC.visibility_of_element_located(self.textbox_email))
        txtbox.clear()
        txtbox.send_keys(mail)

    def send_telephone(self, telephone: str):
        txtbox = self.wait.until(EC.visibility_of_element_located(self.textbox_telephone))
        txtbox.clear()
        txtbox.send_keys(telephone)

    def send_password(self, password: str):
        txtbox = self.wait.until(EC.visibility_of_element_located(self.textbox_password))
        txtbox.clear()
        txtbox.send_keys(password)

    def send_password_confirm(self, password_confirm: str):
        txtbox = self.wait.until(EC.visibility_of_element_located(self.textbox_confirm_password))
        txtbox.clear()
        txtbox.send_keys(password_confirm)

    def click_no_subscribe(self):
        radio = self.wait.until(EC.element_to_be_clickable(self.radio_no_subscribe))
        radio.click()

    def click_yes_subscribe(self):
        radio = self.wait.until(EC.element_to_be_clickable(self.radio_yes_subscribe))
        radio.click()

    def click_agree_terms(self):
        checkbox = self.wait.until(EC.element_to_be_clickable(self.checkbox_agree))
        checkbox.click()

    def click_continue(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.btn_continue))
        btn.click()

    def get_confirm_account_msg(self):
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.text_msg_conf))
            return element.text

        except Exception as e:
            # print(f"Failed to get confirm account msg: {e}")
            logger.error(f"[get_confirm_account_msg]: Failed to get confirm account msg: {e}")
            return None

    def get_error_missing_checkbox_agree_policy(self):
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.text_warning_not_agreed_to_policy))
            return element.text

        except Exception as e:
            # print(f"Failed to get missing checkbox agreement msg: {e}")
            logger.error(f"[get_error_missing_checkbox_agree_policy]: Failed to get missing checkbox agreement msg: {e}")
            return None

    def get_error_passwords_mismatch(self):
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.text_err_passwords_mismatch))
            return element.text

        except Exception as e:
            # print(f"Failed to get passwords mismatch msg: {e}")
            logger.error(f"[get_error_passwords_mismatch]: Failed to get passwords mismatch msg: {e}")
            return None

    def get_register_account_text(self):
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.text_register_acc))
            return element.text

        except Exception as e:
            # print(f"Failed to get register_acc text: {e}")
            logger.error(f"[get_register_account_text]: Failed to get register_acc text: {e}")
            return None


