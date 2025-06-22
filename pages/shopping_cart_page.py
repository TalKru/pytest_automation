import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys


class ShoppingCartPage:

    btn_checkout = (By.XPATH, "//a[@class='btn btn-primary']")
    btn_shopping_cart = (By.XPATH, "//span[normalize-space()='Shopping Cart']")
    btn_update_quantity = (By.XPATH, ".//button[@data-original-title='Update']")
    btns_remove_items = (By.XPATH, "//button[@class='btn btn-danger']")
    table_cart_items_list = (By.XPATH, "//div[@class='table-responsive']//tbody")
    textbox_quantity = (By.XPATH, ".//input[contains(@name,'quantity[')]")

    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    def get_amount_of_items_in_cart(self) -> int:
        """
        Returns how many rows (items) are in the cart table.
        If the cart is empty (no table body found), returns 0.
        """
        # Attempt to find any table bodies that match your locator
        cart_bodies = self.driver.find_elements(*self.table_cart_items_list)

        if not cart_bodies:
            # No table body found => empty cart
            return 0

        tbody_element = cart_bodies[0]
        rows = tbody_element.find_elements(By.TAG_NAME, "tr")
        return len(rows)

    def click_checkout_btn(self):
        element = self.wait.until(EC.element_to_be_clickable(self.btn_checkout))
        element.click()

    def click_shopping_cart_btn(self):
        element = self.wait.until(EC.element_to_be_clickable(self.btn_shopping_cart))
        element.click()

    def remove_item_by_index(self, index: int):
        """
        Removes the cart item at the given row index.
        """
        # Wait for rows to be present
        rows = self.wait.until(EC.presence_of_all_elements_located(self.btns_remove_items))
        # Locate the remove button in that row and click it
        remove_button = rows[index]
        remove_button.click()
        time.sleep(1.5)  # time to update

    def update_item_quantity(self, new_quantity: int):
        """
        Updates the quantity of the cart item at the given row index, then clicks the update button.
        """
        qty_input = self.wait.until(EC.presence_of_element_located(self.textbox_quantity))
        qty_input.clear()
        qty_input.send_keys(str(new_quantity))

        # Click the "Update" button (often has a refresh icon or 'data-original-title="Update"')
        update_button = self.wait.until(EC.presence_of_element_located(self.btn_update_quantity))
        update_button.click()
        time.sleep(1.5)  # brief wait for the update to apply

    def get_item_quantity(self) -> int:
        """
        Returns the current quantity of the cart item at the given row index.
        """
        qty_input = self.wait.until(EC.presence_of_element_located(self.textbox_quantity))
        return int(qty_input.get_attribute("value"))





