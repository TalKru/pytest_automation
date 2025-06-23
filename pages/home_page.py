import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys


class HomePage:
    # url = "https://naveenautomationlabs.com/opencart/"
    btn_my_account = (By.XPATH, "//a[@title='My Account']")
    btn_register = (By.XPATH, "//a[normalize-space()='Register']")
    btn_login = (By.XPATH, "//a[normalize-space()='Login']")
    btn_shopping_cart = (By.XPATH, "//a[@title='Shopping Cart']")
    btn_checkout = (By.XPATH, "//a[@title='Checkout']")
    btn_laptops_dropdown = (By.XPATH, "//a[normalize-space()='Laptops & Notebooks']")
    btn_laptops_menu = (By.XPATH, "//a[normalize-space()='Show All Laptops & Notebooks']")
    dropdown_mp3_menu = (By.XPATH, "//a[text()='MP3 Players']")
    btn_mp3_page = (By.XPATH, "//a[text()='Show All MP3 Players']")

    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver  # build the obj with driver obj from the test case
        self.wait = wait

    def click_my_account(self):
        my_acc_btn = self.wait.until(EC.element_to_be_clickable(self.btn_my_account))
        my_acc_btn.click()

    def click_register(self):
        register_btn = self.wait.until(EC.element_to_be_clickable(self.btn_register))
        register_btn.click()

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.btn_login))
        login_btn.click()

    def click_shopping_cart(self):
        shopping_cart_btn = self.wait.until(EC.element_to_be_clickable(self.btn_shopping_cart))
        shopping_cart_btn.click()

    def click_checkout(self):
        checkout_btn = self.wait.until(EC.element_to_be_clickable(self.btn_checkout))
        checkout_btn.click()

    def click_laptops_dropdown_options(self):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.btn_laptops_dropdown))
        dropdown.click()

    def click_laptops_menu(self):
        laptops_btn = self.wait.until(EC.element_to_be_clickable(self.btn_laptops_menu))
        laptops_btn.click()

    def click_mp3_menu(self):
        dropdown_players_btn = self.wait.until(EC.element_to_be_clickable(self.dropdown_mp3_menu))
        dropdown_players_btn.click()
        time.sleep(0.1)

        btn_player_page = self.wait.until(EC.element_to_be_clickable(self.btn_mp3_page))
        btn_player_page.click()


