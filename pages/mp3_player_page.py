from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys
# from selenium.webdriver.common.action_chains import ActionChains
import time
import re


class MP3Page:

    CURRENCY_EUR = (By.XPATH, "//button[@type='button' and @name='EUR']")
    CURRENCY_GBP = (By.XPATH, "//button[@type='button' and @name='GBP']")
    CURRENCY_USD = (By.XPATH, "//button[@type='button' and @name='USD']")
    _OPTIONS = {
        'EUR': CURRENCY_EUR,
        'GBP': CURRENCY_GBP,
        'USD': CURRENCY_USD,
    }
    #all_showing_items = (By.XPATH, "//span[text()='Add to Cart']")
    all_showing_items = (By.XPATH, "//span[@class='hidden-xs hidden-sm hidden-md' and normalize-space(.)='Add to Cart']")
    all_text_prices = (By.XPATH, "//p[@class='price']")
    btn_cart = (By.XPATH, "//*[@id='cart-total']")
    toggle_currency = (By.XPATH, "//form[@id='form-currency']//button[contains(@class,'dropdown-toggle')]")

    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    def open_currency_menu(self):
        """Clicks the currency toggle to reveal the list."""
        toggle = self.wait.until(EC.element_to_be_clickable(self.toggle_currency))
        toggle.click()

    def select_currency(self, currency: str):
        """
        Chooses one of the supported currencies.
        :param currency: One of 'EUR', 'GBP', 'USD'
        :raises KeyError: if you pass an unsupported code
        """
        if currency not in self._OPTIONS:
            raise ValueError(f"Unsupported currency '{currency}'. Must be one of {self._OPTIONS}")

        self.open_currency_menu()
        time.sleep(0.2)
        locator = self._OPTIONS[currency]
        btn = self.wait.until(EC.visibility_of_element_located(locator))
        btn.click()
        time.sleep(0.2)

    def get_total_price_of_showing_items(self) -> float:
        """
        Find all <p class="price"> elements on the page,
        extract the numeric part of their text (e.g. "95.72") and sum them.
        """
        price_elements = self.wait.until(EC.presence_of_all_elements_located(self.all_text_prices))
        total_sum: float = 0.0

        for elem in price_elements:
            raw_text = elem.text.strip()  # remove leading/trailing whitespace/newlines
            m = re.search(r"[-+]?\d*\.\d+|\d+", raw_text)  # extract the first numeric sequence (int or decimal)
            if m:
                total_sum += float(m.group())  # .group() returns the exact substring that matched, for example "95.72"

        return total_sum

    def add_all_mp3_to_cart(self):
        # grab the initial list to know how many buttons there are
        buttons = self.wait.until(EC.presence_of_all_elements_located(self.all_showing_items))
        total = len(buttons)

        # loop by index so we can re-fetch the list each time (avoids staleness)
        for i in range(total):
            # re-locate current buttons
            buttons = self.wait.until(EC.presence_of_all_elements_located(self.all_showing_items))
            btn = buttons[i]
            time.sleep(0.2)

            ActionChains(self.driver).move_to_element(btn).perform()

            self.wait.until(EC.element_to_be_clickable(self.all_showing_items))
            btn.click()
            time.sleep(0.5)

    def click_go_to_cart(self):
        btn = self.wait.until(EC.visibility_of_element_located(self.btn_cart))
        btn.click()

    def get_cart_btn_info(self) -> str:
        btn_info = self.wait.until(EC.visibility_of_element_located(self.btn_cart))
        return btn_info.text.strip()



