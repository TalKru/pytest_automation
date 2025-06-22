import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys


class LaptopsPage:
    # url = "https://naveenautomationlabs.com/opencart/index.php?route=product/category&path=18"
    linktext_item_HPLP3065 = (By.XPATH, "//a[normalize-space()='HP LP3065']")
    linktext_item_MacBook = (By.XPATH, "//a[normalize-space()='MacBook']")
    linktext_item_SonyVAIO = (By.XPATH, "//a[normalize-space()='Sony VAIO']")
    btn_add_to_cart = (By.XPATH, "//button[@id='button-cart']")                    # same locator for all items
    btn_shopping_cart = (By.XPATH, "//span[normalize-space()='Shopping Cart']")
    textbox_amount = (By.XPATH, "//input[@id='input-quantity']")                   # same locator for all items

    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver  # build the obj with driver obj from the test case
        self.wait = wait

    def open_item_new_tab_add_close(self, locator, amount: int):
        """Open the product link in a new tab, set quantity, add to cart, then close."""
        elem = self.wait.until(EC.presence_of_element_located(locator))

        # CTRL+ENTER opens in new tab
        elem.send_keys(Keys.CONTROL + Keys.ENTER)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(0.2)

        # set qty and click “Add to Cart”
        self.select_amount_of_items(amount)
        btn_add_to_cart = self.wait.until(EC.element_to_be_clickable(self.btn_add_to_cart))
        btn_add_to_cart.click()
        time.sleep(0.2)

        # close tab and return focus
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def select_amount_of_items(self, amount: int):
        element = self.wait.until(EC.visibility_of_element_located(self.textbox_amount))
        element.clear()
        element.send_keys(str(amount))

    def click_hp_laptop_link(self):
        element = self.wait.until(EC.visibility_of_element_located(self.linktext_item_HPLP3065))
        element.click()

    def click_apple_laptop_link(self):
        element = self.wait.until(EC.visibility_of_element_located(self.linktext_item_MacBook))
        element.click()

    def click_sony_laptop_link(self):
        element = self.wait.until(EC.visibility_of_element_located(self.linktext_item_SonyVAIO))
        element.click()

    def click_shopping_cart(self):
        element = self.wait.until(EC.visibility_of_element_located(self.btn_shopping_cart))
        element.click()

    def click_add_to_cart(self):
        element = self.wait.until(EC.visibility_of_element_located(self.btn_add_to_cart))
        element.click()

