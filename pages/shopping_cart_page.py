import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys


class ShoppingCartPage:
    btn_checkout_xpath = "//a[@class='btn btn-primary']"
    btn_shopping_cart_xpath = "//span[normalize-space()='Shopping Cart']"
    btn_update_quantity_xpath = ".//button[@data-original-title='Update']"
    btns_remove_items_xpath = "//button[@class='btn btn-danger']"

    table_cart_items_list_xpath = "//div[@class='table-responsive']//tbody"

    textbox_quantity_xpath = ".//input[contains(@name,'quantity[')]"

    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    # def get_amount_of_items_in_cart(self) -> int:
    #     # 1. Locate the table body
    #     tbody_element = self.driver.find_element(By.XPATH, self.table_cart_items_list_xpath)
    #     # 2. Find all rows (<tr>) within that tbody
    #     rows = tbody_element.find_elements(By.TAG_NAME, "tr")
    #     return len(rows)

    def get_amount_of_items_in_cart(self) -> int:
        """
        Returns how many rows (items) are in the cart table.
        If the cart is empty (no table body found), returns 0.
        """
        # Attempt to find any table bodies that match your locator
        cart_bodies = self.driver.find_elements(By.XPATH, self.table_cart_items_list_xpath)
        if not cart_bodies:
            # No table body found => empty cart
            return 0

        tbody_element = cart_bodies[0]
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

    def remove_item_by_index(self, index: int):
        """
        Removes the cart item at the given row index.
        """
        # Wait for rows to be present
        rows = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.btns_remove_items_xpath)))
        # Locate the remove button in that row and click it
        remove_button = rows[index]
        remove_button.click()
        time.sleep(1.5)  # time to update

    def update_item_quantity(self, new_quantity: int):
        """
        Updates the quantity of the cart item at the given row index, then clicks the update button.
        """
        qty_input = self.wait.until(EC.presence_of_element_located((By.XPATH, self.textbox_quantity_xpath)))
        qty_input.clear()
        qty_input.send_keys(str(new_quantity))

        # Click the "Update" button (often has a refresh icon or 'data-original-title="Update"')
        update_button = self.wait.until(EC.presence_of_element_located((By.XPATH, self.btn_update_quantity_xpath)))
        update_button.click()

        time.sleep(1.5)  # brief wait for the update to apply

    def get_item_quantity(self) -> int:
        """
        Returns the current quantity of the cart item at the given row index.
        """
        qty_input = self.wait.until(EC.presence_of_element_located((By.XPATH, self.textbox_quantity_xpath)))
        return int(qty_input.get_attribute("value"))





