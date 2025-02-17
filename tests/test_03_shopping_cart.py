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
    try:
        home_page_obj = HomePage(driver, wait)
        laptops_page_obj = LaptopsPage(driver, wait)
        shopping_cart_obj = ShoppingCartPage(driver, wait)

        driver.get(DATA.get_home_url())
        logger.info(f"[{test_context}] loaded page url")

        # open items - laptops
        home_page_obj.click_laptops_dropdown_options()
        home_page_obj.click_laptops_menu()
        logger.info(f"[{test_context}] click_laptops_menu")

        # add 3 laptops to the cart
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

