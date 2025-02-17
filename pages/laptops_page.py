from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys


class LaptopsPage:
    # url = "https://naveenautomationlabs.com/opencart/index.php?route=product/category&path=18"
    linktext_item_HPLP3065_xpath = "//a[normalize-space()='HP LP3065']"
    linktext_item_MacBook_xpath = "//a[normalize-space()='MacBook']"
    linktext_item_SonyVAIO_xpath = "//a[normalize-space()='Sony VAIO']"

    btn_add_to_cart_xpath = "//button[@id='button-cart']"   # same locator for all items
    btn_shopping_cart_xpath = "//span[normalize-space()='Shopping Cart']"

    textbox_amount_xpath = "//input[@id='input-quantity']"  # same locator for all items

    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver  # build the obj with driver obj from the test case
        self.wait = wait

    def get_locate_tup_hp_laptop_link(self) -> tuple[str, str]:
        return (By.XPATH, self.linktext_item_HPLP3065_xpath)

    def get_locate_tup_apple_laptop_link(self) -> tuple[str, str]:
        return (By.XPATH, self.linktext_item_MacBook_xpath)

    def get_locate_tup_sony_laptop_link(self) -> tuple[str, str]:
        return (By.XPATH, self.linktext_item_SonyVAIO_xpath)

    def click_hp_laptop_link(self):
        tup = (By.XPATH, self.linktext_item_HPLP3065_xpath)
        element = self.wait.until(EC.visibility_of_element_located(tup))
        element.click()

    def click_apple_laptop_link(self):
        tup = (By.XPATH, self.linktext_item_MacBook_xpath)
        element = self.wait.until(EC.visibility_of_element_located(tup))
        element.click()

    def click_sony_laptop_link(self):
        tup = (By.XPATH, self.linktext_item_SonyVAIO_xpath)
        element = self.wait.until(EC.visibility_of_element_located(tup))
        element.click()

    def click_shopping_cart(self):
        tup = (By.XPATH, self.btn_shopping_cart_xpath)
        element = self.wait.until(EC.visibility_of_element_located(tup))
        element.click()

    def click_add_to_cart(self):
        tup = (By.XPATH, self.btn_add_to_cart_xpath)
        element = self.wait.until(EC.visibility_of_element_located(tup))
        element.click()

    def select_amount_of_items(self, amount: int):
        tup = (By.XPATH, self.textbox_amount_xpath)
        element = self.wait.until(EC.visibility_of_element_located(tup))
        element.clear()
        element.send_keys(str(amount))


