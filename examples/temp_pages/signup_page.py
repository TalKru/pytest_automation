from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys


class SignupPage:
    radio_select_male_xpath = "//input[@id='id_gender1']"
    radio_select_female_xpath = "//input[@id='id_gender2']"
    textbox_password_xpath = "//input[@id='password']"
    textbox_firstname_xpath = "//input[@id='first_name']"
    textbox_lastname_xpath = "//input[@id='last_name']"
    textbox_address_xpath = "//input[@id='address1']"
    select_country_xpath = "//select[@id='country']"
    textbox_state_xpath = "//input[@id='state']"
    textbox_city_xpath = "//input[@id='city']"
    textbox_zip_xpath = "//input[@id='zipcode']"
    textbox_mobile_num_xpath = "//input[@id='mobile_number']"
    btn_create_account_xpath = "//button[normalize-space()='Create Account']"

    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver  # build the obj with driver obj from the test case
        self.wait = wait

    def click_male(self):
        locate_tup = (By.XPATH, self.radio_select_male_xpath)
        self.wait.until(EC.element_to_be_clickable(locate_tup)).click()

    def click_female(self):
        locate_tup = (By.XPATH, self.radio_select_female_xpath)
        self.wait.until(EC.element_to_be_clickable(locate_tup)).click()

    def send_password(self, password: str):
        locate_tup = (By.XPATH, self.textbox_password_xpath)
        textbox = self.wait.until(EC.presence_of_element_located(locate_tup))
        textbox.clear()
        textbox.send_keys(password)









