from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys


class CheckoutPage:
    # url = "https://naveenautomationlabs.com/opencart/"
    dropdown_currency = (By.XPATH, "//form[@id='form-currency']")  # "//span[normalize-space()='Currency']"
    dropdown_options = (By.XPATH, "//ul[@class='dropdown-menu']/li/button")
    text_currency_type = (By.XPATH, "//span[@id='cart-total']")   # also items amount count

    def __init__(self, driver: webdriver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    def click_currency_btn(self):
        element = self.wait.until(EC.visibility_of_element_located(self.dropdown_currency))
        element.click()

    def get_list_of_currency_options(self) -> list[str]:
        """
        Make sure you DO CLICK the function "click_currency_btn" before invoking this function,
        or it will fail to locate the element
        """
        # self.click_currency_btn() # assume it happened!
        currency_options = []
        menu_element = self.wait.until(EC.visibility_of_all_elements_located(self.dropdown_options))

        for currency_option in menu_element:
            if currency_option is not None:
                # currency_options.append(currency_option.get_attribute("name")) # ['EUR', 'GBP', 'USD']
                currency_options.append(currency_option.text)  # ['€ Euro', '£ Pound Sterling', '$ US Dollar']
        return currency_options


"""
1. Correct XPath for Options:
self.dropdown_options_xpath = "//ul[@class='dropdown-menu']/li/button": This is the critical change. 
Instead of targeting the <ul> element, this XPath targets all the **<button>** elements 
that are direct children of <li> elements, which are themselves children of the <ul> with class='dropdown-menu'. 
These are the actual clickable elements containing the text.

2. visibility_of_all_elements_located is used correctly:
Now, options_elements will be a list of all the button WebElements, which is what you want to iterate over.

3. Extracting the Correct Value:
name_attribute = option_element.get_attribute("name"): This will correctly retrieve the name attribute 
(e.g., "EUR", "GBP", "USD") from each <button> element.
If you need the visible text like "€ Euro", you would use option_element.text. 
"""



