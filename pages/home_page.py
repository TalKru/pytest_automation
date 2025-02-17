from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys


class HomePage:
    # locators
    # url = "https://naveenautomationlabs.com/opencart/"
    btn_my_account_xpath = "//a[@title='My Account']"
    btn_register_xpath = "//a[normalize-space()='Register']"
    btn_login_xpath = "//a[normalize-space()='Login']"
    btn_shopping_cart_xpath = "//a[@title='Shopping Cart']"
    btn_checkout_xpath = "//a[@title='Checkout']"
    btn_laptops_dropdown_xpath = "//a[normalize-space()='Laptops & Notebooks']"
    btn_laptops_menu_xpath = "//a[normalize-space()='Show All Laptops & Notebooks']"

    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver  # build the obj with driver obj from the test case
        self.wait = wait

    def click_my_account(self):
        tup = (By.XPATH, self.btn_my_account_xpath)
        my_acc_btn = self.wait.until(EC.element_to_be_clickable(tup))
        my_acc_btn.click()

    def click_register(self):
        tup = (By.XPATH, self.btn_register_xpath)
        register_btn = self.wait.until(EC.element_to_be_clickable(tup))
        register_btn.click()

    def click_login(self):
        tup = (By.XPATH, self.btn_login_xpath)
        login_btn = self.wait.until(EC.element_to_be_clickable(tup))
        login_btn.click()

    def click_shopping_cart(self):
        tup = (By.XPATH, self.btn_shopping_cart_xpath)
        shopping_cart_btn = self.wait.until(EC.element_to_be_clickable(tup))
        shopping_cart_btn.click()

    def click_checkout(self):
        tup = (By.XPATH, self.btn_checkout_xpath)
        checkout_btn = self.wait.until(EC.element_to_be_clickable(tup))
        checkout_btn.click()

    def click_laptops_dropdown_options(self):
        tup = (By.XPATH, self.btn_laptops_dropdown_xpath)
        checkout_btn = self.wait.until(EC.element_to_be_clickable(tup))
        checkout_btn.click()

    def click_laptops_menu(self):
        tup = (By.XPATH, self.btn_laptops_menu_xpath)
        checkout_btn = self.wait.until(EC.element_to_be_clickable(tup))
        checkout_btn.click()


