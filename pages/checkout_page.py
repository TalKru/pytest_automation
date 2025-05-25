from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys


class CheckoutPage:
    # locators
    # url = "https://naveenautomationlabs.com/opencart/"
    dropdown_currency_xpath = "//form[@id='form-currency']"  # "//span[normalize-space()='Currency']"
    dropdown_options_xpath = "//ul[@class='dropdown-menu']/li/button"
    text_currency_type_xpath = "//span[@id='cart-total']"  # also items amount count

    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    def click_currency_btn(self):
        tup = (By.XPATH, self.dropdown_currency_xpath)
        element = self.wait.until(EC.visibility_of_element_located(tup))
        element.click()

    def get_list_of_currency_options(self) -> list[str]:
        """
        Make sure you DO CLICK the function "click_currency_btn" before invoking this function,
        or it will fail to locate the element
        """
        # self.click_currency_btn() # assume it happened!
        currency_options = []
        tup = (By.XPATH, self.dropdown_options_xpath)
        menu_element = self.wait.until(EC.visibility_of_all_elements_located(tup))

        for currency_option in menu_element:
            # currency_options.append(currency_option.get_attribute("name")) # ['EUR', 'GBP', 'USD']
            currency_options.append(currency_option.text)                    # ['€ Euro', '£ Pound Sterling', '$ US Dollar']
        return currency_options






