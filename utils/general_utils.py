import os
import pytest
from selenium import webdriver
import random


def capture_screenshot(driver: webdriver, request):
    """
    Capture a screenshot and save it using the test's node ID format.
    possible to modify both the:
    screenshot name --> screenshot_filename
    screenshot path to save --> screenshot_path
    must be adjusted to the fixture "pytest_runtest_makereport" from the conftest.py file
    """

    # Get the test file path and function name
    test_path_parts: str = request.node.nodeid.split("::")
    test_file = test_path_parts[0]       # e.g., "examples/test_simple_login.py"
    # test_file.split("/")[1]            # e.g., "test_simple_login.py"
    test_name = test_path_parts[1]       # e.g., "test_logo"

    # Construct the desired path structure
    screenshot_filename = f"{test_file.split("/")[1]}_{test_name}.png".replace("/", "_").replace("\\", "_")
    screenshot_path = os.path.join("reports", test_file.split('/')[0], screenshot_filename)

    os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)  # Ensure the directory exists

    driver.save_screenshot(screenshot_path)

    return screenshot_path  # Return for debugging/logging


def generate_random_email(min_range=10000, max_range=99999, prefix="temp", suffix="@supermail.com") -> str:
    """Generate a random email address with random digits."""
    random_number = random.randint(min_range, max_range)  # Generates a random 5-digit number
    email = prefix + str(random_number) + suffix
    return email
