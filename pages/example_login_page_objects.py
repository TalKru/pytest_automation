
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys


class LoginPage:
    # locators - OF A SINGLE PAGE
    input_username_id = 'username'
    input_password_id = 'password'
    btn_submit_id = 'submit'

    # constructor
    def __init__(self, driver: webdriver):
        self.driver = driver  # build the obj with driver obj from the test case

    # action methods
    def send_username(self, username: str):
        username_box = self.driver.find_element(By.ID, self.input_username_id)
        username_box.clear()
        username_box.send_keys(username)

    def send_password(self, password: str):
        password_box = self.driver.find_element(By.ID, self.input_password_id)
        password_box.clear()
        password_box.send_keys(password)

    def click_login(self):
        login_btn = self.driver.find_element(By.ID, self.btn_submit_id)
        login_btn.click()



