# ---------------------------------------------------------------------------------------------------------- #
import pytest

from pages.home_page import HomePage          # "HomePage" is a class with all the locators and funcs
from pages.login_page import LoginPage
from pages.laptops_page import LaptopsPage
from pages.shopping_cart_page import ShoppingCartPage
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
import requests


# @pytest.mark.skip
@pytest.mark.sanity
def test_add_items_to_cart(driver, wait, request, test_context):
    """
    Test Case: Add multiple laptop items to the shopping cart and verify item count.
    Steps:
    1. Navigate to the home page.
    2. Open the laptops category and load the laptops listing.
    3. Open each laptop in a new tab, add a specified quantity to the cart, then close the tab.
    4. Navigate to the shopping cart and verify the correct number of unique laptop types are added.
    Expected Result:
    - The shopping cart should contain exactly 3 different laptop types.
    """
    try:
        home_page_obj = HomePage(driver, wait)
        laptops_page_obj = LaptopsPage(driver, wait)
        shopping_cart_obj = ShoppingCartPage(driver, wait)

        driver.get(DATA.get_home_url())
        logger.info(f"[{test_context}] loaded page url")

        # Navigate to laptops
        home_page_obj.click_laptops_dropdown_options()
        home_page_obj.click_laptops_menu()
        logger.info(f"[{test_context}] Navigated to laptops menu")

        # Prepare locators for 3 laptops
        locator_tup_item_1 = laptops_page_obj.get_locate_tup_apple_laptop_link()
        locator_tup_item_2 = laptops_page_obj.get_locate_tup_hp_laptop_link()
        locator_tup_item_3 = laptops_page_obj.get_locate_tup_sony_laptop_link()

        button_1 = wait.until(EC.presence_of_element_located(locator_tup_item_1))
        button_2 = wait.until(EC.presence_of_element_located(locator_tup_item_2))
        button_3 = wait.until(EC.presence_of_element_located(locator_tup_item_3))

        keys_combo = Keys.CONTROL + Keys.ENTER

        # -------------------------------------------------------------------------------------------->
        button_1.send_keys(keys_combo)
        logger.info(f"[{test_context}] new tab for item 1")

        driver.switch_to.window(driver.window_handles[1])
        logger.info(f"[{test_context}] switch driver focus on the new tab")

        laptops_page_obj.select_amount_of_items(4)
        logger.info(f"[{test_context}] selected amount of items: 4")

        laptops_page_obj.click_add_to_cart()
        logger.info(f"[{test_context}] items added to cart")

        driver.close()  # close current tab
        logger.info(f"[{test_context}] tab is closed")

        driver.switch_to.window(driver.window_handles[0])
        logger.info(f"[{test_context}] switch focus back to main tab page")
        # -------------------------------------------------------------------------------------------->
        button_2.send_keys(keys_combo)
        logger.info(f"[{test_context}] new tab for item 2")

        driver.switch_to.window(driver.window_handles[1])
        logger.info(f"[{test_context}] switch focus back to item tab ")

        laptops_page_obj.select_amount_of_items(3)
        logger.info(f"[{test_context}] selected amount of items: 3")

        laptops_page_obj.click_add_to_cart()
        logger.info(f"[{test_context}] items added to cart")

        driver.close()
        logger.info(f"[{test_context}] tab is closed")

        driver.switch_to.window(driver.window_handles[0])  # switch focus back to main page
        logger.info(f"[{test_context}] switch focus back to main tab page")
        # -------------------------------------------------------------------------------------------->
        button_3.send_keys(keys_combo)
        logger.info(f"[{test_context}] new tab for item 3")
        driver.switch_to.window(driver.window_handles[1])
        logger.info(f"[{test_context}] switch focus back to item tab ")
        laptops_page_obj.select_amount_of_items(1)
        logger.info(f"[{test_context}] selected amount of items: 1")
        laptops_page_obj.click_add_to_cart()
        logger.info(f"[{test_context}] items added to cart")
        driver.close()
        logger.info(f"[{test_context}] tab is closed")
        driver.switch_to.window(driver.window_handles[0])
        logger.info(f"[{test_context}] switch focus back to main tab page")
        # -------------------------------------------------------------------------------------------->

        laptops_page_obj.click_shopping_cart()
        logger.info(f"[{test_context}] click_shopping_cart")

        items_amount = shopping_cart_obj.get_amount_of_items_in_cart()
        logger.info(f"[{test_context}] {items_amount=}")

        expected_item_types = 3
        logger.info(f"[{test_context}] {expected_item_types=}")
        assert items_amount == expected_item_types

    except Exception as e:
        capture_screenshot(driver, request)
        logger.error(f"[{test_context}] test failed: {e}")
        pytest.fail(f"Test failed due to: {e}")


@pytest.mark.regression
def test_remove_item_from_cart(driver, wait, request, test_context):
    """
    Test Case: Add one laptop to the cart, remove it, then verify the cart is empty.
    Steps:
    1. Navigate to the home page and open laptops.
    2. Add a single laptop to the cart.
    3. Navigate to the shopping cart and remove the item.
    4. Verify the cart is empty (0 items).
    Expected Result:
    - The cart should have 0 items after removal.
    """
    try:
        home_page_obj = HomePage(driver, wait)
        laptops_page_obj = LaptopsPage(driver, wait)
        shopping_cart_obj = ShoppingCartPage(driver, wait)

        # 1. Navigate to home, then open laptops
        driver.get(DATA.get_home_url())
        logger.info(f"[{test_context}] Loaded home page")

        home_page_obj.click_laptops_dropdown_options()
        logger.info(f"[{test_context}] Clicked 'Laptops & Notebooks' dropdown")

        home_page_obj.click_laptops_menu()
        logger.info(f"[{test_context}] Selected 'Show All Laptops & Notebooks'")

        # 2. Add a single laptop (HP) to the cart
        laptops_page_obj.click_hp_laptop_link()
        logger.info(f"[{test_context}] Clicked HP laptop link")

        laptops_page_obj.select_amount_of_items(1)
        logger.info(f"[{test_context}] Selected quantity: 1")

        laptops_page_obj.click_add_to_cart()
        logger.info(f"[{test_context}] Added HP laptop to cart")

        # 3. Navigate to cart, remove the item
        laptops_page_obj.click_shopping_cart()
        logger.info(f"[{test_context}] Navigated to Shopping Cart")

        shopping_cart_obj.remove_item_by_index(0)
        logger.info(f"[{test_context}] Removed item at index 0")

        # 4. Verify cart is empty
        item_count = shopping_cart_obj.get_amount_of_items_in_cart()
        logger.info(f"[{test_context}] Cart item count = {item_count}")

        assert item_count == 0, f"Expected empty cart, found {item_count} items."

    except Exception as e:
        capture_screenshot(driver, request)
        logger.error(f"[{test_context}] test failed: {e}")
        pytest.fail(f"Test failed due to: {e}")


@pytest.mark.regression
def test_update_item_quantity_in_cart(driver, wait, request, test_context):
    """
    Test Case: Update the quantity of an item in the shopping cart.

    Steps:
    1. Navigate to the home page and open the laptops section.
    2. Add a single laptop to the cart (quantity=1).
    3. Go to the shopping cart page.
    4. Update the laptop's quantity to 3.
    5. Verify the quantity is updated to 3.

    Expected Result:
    - The item's quantity in the cart should be exactly 3.
    """
    try:
        home_page_obj = HomePage(driver, wait)
        laptops_page_obj = LaptopsPage(driver, wait)
        shopping_cart_obj = ShoppingCartPage(driver, wait)

        # 1. Navigate to home, open laptops
        driver.get(DATA.get_home_url())
        logger.info(f"[{test_context}] Loaded home page")

        home_page_obj.click_laptops_dropdown_options()
        logger.info(f"[{test_context}] Clicked 'Laptops & Notebooks' dropdown")

        home_page_obj.click_laptops_menu()
        logger.info(f"[{test_context}] Selected 'Show All Laptops & Notebooks'")

        # 2. Add one laptop with quantity=1
        laptops_page_obj.click_hp_laptop_link()
        logger.info(f"[{test_context}] Clicked HP laptop link")

        laptops_page_obj.select_amount_of_items(1)
        logger.info(f"[{test_context}] Set quantity to 1")

        laptops_page_obj.click_add_to_cart()
        logger.info(f"[{test_context}] Added HP laptop to cart")

        # 3. Go to the shopping cart page
        laptops_page_obj.click_shopping_cart()
        logger.info(f"[{test_context}] Navigated to Shopping Cart")

        # 4. Update the laptop's quantity to 3
        shopping_cart_obj.update_item_quantity(3)
        logger.info(f"[{test_context}] Updated item quantity at index 0 to 3")

        # 5. Verify the quantity is updated to 3
        actual_qty = shopping_cart_obj.get_item_quantity()
        logger.info(f"[{test_context}] Actual item quantity: {actual_qty}")

        assert actual_qty == 3, f"Expected quantity=3, but found {actual_qty}"

    except Exception as e:
        capture_screenshot(driver, request)
        logger.error(f"[{test_context}] test failed: {e}")
        pytest.fail(f"Test failed due to: {e}")
