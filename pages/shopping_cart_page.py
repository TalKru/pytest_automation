from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys


class ShoppingCartPage:
    btn_checkout_xpath = "//a[@class='btn btn-primary']"
    btn_shopping_cart_xpath = "//span[normalize-space()='Shopping Cart']"

    table_cart_items_list_xpath = "//div[@class='table-responsive']//tbody"

    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    def get_amount_of_items_in_cart(self) -> int:
        # 1. Locate the table body
        tbody_element = self.driver.find_element(By.XPATH, self.table_cart_items_list_xpath)

        # 2. Find all rows (<tr>) within that tbody
        rows = tbody_element.find_elements(By.TAG_NAME, "tr")
        return len(rows)

    def click_checkout_btn(self):
        tup = (By.XPATH, self.btn_checkout_xpath)
        element = self.wait.until(EC.element_to_be_clickable(tup))
        element.click()

    def click_shopping_cart_btn(self):
        tup = (By.XPATH, self.btn_shopping_cart_xpath)
        element = self.wait.until(EC.element_to_be_clickable(tup))
        element.click()







