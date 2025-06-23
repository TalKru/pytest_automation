# ---------------------------------------------------------------------------------------------------------- #
import pytest

from pages.home_page import HomePage          # "HomePage" is a class with all the locators and funcs
from pages.checkout_page import CheckoutPage
from pages.mp3_player_page import MP3Page
# ---------------------------------------------------------------------------------------------------------- #
from utils.logger import logger
from utils.general_utils import generate_random_email
from utils.general_utils import capture_screenshot
from utils import read_config_data as DATA
# ---------------------------------------------------------------------------------------------------------- #
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
# ---------------------------------------------------------------------------------------------------------- #
# conftest is imported seamlessly by pytest
import time


@pytest.mark.regression
def test_mp3_players_cart_count_and_total_price(driver, wait, request, test_context):
    """
    Test Case: Add every MP3 player on the listing page to the shopping cart,
    then verify that:
      1. The cart button’s text shows the correct number of items added.
      2. The sum of the individual prices (as displayed on the page before adding)
         exactly matches the expected total.

    Steps:
    1. Navigate to the home page.
    2. Go to the “MP3 Players” category.
    3. Select “EUR” as the currency.
    4. Add all visible MP3 items to the cart.
    5. Read the “cart” button text to confirm the item count.
    6. Iterate through all displayed prices, extract and sum them.
    7. Assert that the cart count is 4 and the summed total equals 382.88 EUR.

    Expected Results:
    - The cart button text contains “4 item(s)”.
    - The computed total price of all MP3 players is exactly 382.88.
    """
    home_page_obj = HomePage(driver, wait)
    mp3_page_obj = MP3Page(driver, wait)
    try:
        logger.info(f"[{test_context}] Init page objects for the test case")

        # 1. Load home page
        driver.get(DATA.get_home_url())
        logger.info(f"[{test_context}] Loaded page URL")

        # 2. Navigate to MP3 Players section
        home_page_obj.click_mp3_menu()
        logger.info(f"[{test_context}] Navigated to MP3 Players page")

        # 3. Switch currency to EUR
        mp3_page_obj.select_currency('EUR')
        logger.info(f"[{test_context}] Selected currency: EUR")

        # 4. Add all MP3 items to the cart
        mp3_page_obj.add_all_mp3_to_cart()
        logger.info(f"[{test_context}] Added all MP3 items to the cart")

        # 5. Verify cart button text shows 4 items
        cart_text: str = mp3_page_obj.get_cart_btn_info()
        logger.info(f"[{test_context}] Cart button shows: {cart_text}")

        assert "4 item(s)" in cart_text, f"Cart text was '{cart_text}', expected '4 item(s)'"

        # 6. Compute total of all individual prices
        total_price: float = mp3_page_obj.get_total_price_of_showing_items()
        logger.info(f"[{test_context}] Computed total price: {total_price}")

        # 7. Assert exact total
        assert total_price == 382.88, f"Summed price was {total_price}, expected 382.88"

    except Exception as e:
        capture_screenshot(driver, request)
        logger.error(f"[{test_context}] test failed: {e}")
        pytest.fail(f"Test failed due to: {e}")


@pytest.mark.smoke
def test_empty_cart_message(driver, wait, request, test_context):
    """
    Test Case: Verify that when you navigate to Checkout with no items in your cart,
    the page shows exactly the empty-cart message.

    Steps:
      1. Go to the home page.
      2. Click the “Checkout” link (which, on OpenCart, will send you to the cart page).
      3. Assert that the browser title is “Shopping Cart”.
      4. Assert that the visible message reads “Your shopping cart is empty!”.

    Expected Result:
      - Title == "Shopping Cart"
      - Empty-cart text == "Your shopping cart is empty!"
    """
    home_page_obj = HomePage(driver, wait)
    checkout_page_obj = CheckoutPage(driver, wait)
    try:
        logger.info(f"[{test_context}] Init page objects for the test case")
        driver.get(DATA.get_home_url())
        logger.info(f"[{test_context}] loaded page url")

        home_page_obj.click_checkout()
        logger.info(f"[{test_context}] navigate to checkout page")

        assert driver.title == "Shopping Cart"
        logger.info(f"[{test_context}] current page <title>: {driver.title}")

        empty_msg: str = checkout_page_obj.get_empty_cart_msg()
        logger.info(f"[{test_context}] extracted text: {empty_msg}")

        assert empty_msg == "Your shopping cart is empty!"

    except Exception as e:
        capture_screenshot(driver, request)
        logger.error(f"[{test_context}] test failed: {e}")
        pytest.fail(f"Test failed due to: {e}")


@pytest.mark.smoke
def test_currency_options(driver, wait, request, test_context):
    """
        Test Case: check if all currency options are available
        1. click currency selector
        2. pull list of all currency options as strings
        3. loop on each option
        4. verify each option is defined in the setup list
        Expected Result:
        - currency should contain exactly 3 different types:
          £ Pound Sterling
          € Euro
          $ US Dollar
        """
    home_page_obj = HomePage(driver, wait)
    checkout_page_obj = CheckoutPage(driver, wait)
    try:
        logger.info(f"[{test_context}] Init page objects for the test case")
        driver.get(DATA.get_home_url())
        logger.info(f"[{test_context}] loaded page url")

        home_page_obj.click_checkout()
        logger.info(f"[{test_context}] navigate to checkout page")

        assert driver.title == "Shopping Cart"
        logger.info(f"[{test_context}] current page <title>: {driver.title}")

        checkout_page_obj.click_currency_btn()
        logger.info(f"[{test_context}] click_currency_btn")

        currency_list = checkout_page_obj.get_list_of_currency_options()
        currency_symbols = ('€', '£', '$')

        logger.info(f"[{test_context}] loop on every currency option and verify it's in the list")
        for option in currency_list:
            currency_symbol = option.split()[0]
            logger.info(f"[{test_context}] ({option}) currency symbol: {currency_symbol}")
            assert currency_symbol in currency_symbols

    except Exception as e:
        capture_screenshot(driver, request)
        logger.error(f"[{test_context}] test failed: {e}")
        pytest.fail(f"Test failed due to: {e}")


