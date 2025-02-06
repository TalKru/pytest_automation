
import pytest
from selenium import webdriver
import random
import string
import os


def capture_screenshot(driver: webdriver, request):
    """
    Capture a screenshot and save it using the test's node ID for naming.
    Screenshots are saved in the absolute path:
        <project_root>/screenshots/<screenshot_filename>
    The filename is built from the test's nodeid (with characters like '::' and '/' replaced
    with underscores), ensuring a unique and valid filename on all OSes.
    """
    # Build a unique screenshot filename from the test's node id.
    # request.node.nodeid returns something like "tests/test_example.py::test_logo"
    # We replace '::' and '/' with '_' to form a valid filename.
    screenshot_filename = f"{request.node.nodeid.replace('::', '_').replace('/', '_').replace('\\', '_')}.png"

    # Define the absolute path to the screenshots folder.
    # os.getcwd() returns the current working directory (the project root)
    screenshots_dir = os.path.join(os.getcwd(), "screenshots")

    # Create the screenshots folder if it does not exist.
    os.makedirs(screenshots_dir, exist_ok=True)

    # Construct the full path for the screenshot file.
    screenshot_path = os.path.join(screenshots_dir, screenshot_filename)

    # Capture the screenshot using the Selenium WebDriver.
    driver.save_screenshot(screenshot_path)
    # TODO logging.info(f"Screenshot saved at: {file_path}")
    return screenshot_path  # Return the path for logging or debugging.


# def capture_screenshot(driver: webdriver, request):
#     """
#     Capture a screenshot and save it using the test's node ID format.
#     possible to modify both the:
#     screenshot name --> screenshot_filename
#     screenshot path to save --> screenshot_path
#     must be adjusted to the fixture "pytest_runtest_makereport" from the conftest.py file
#     """
#     # Get the test file path and function name
#     test_path_parts: str = request.node.nodeid.split("::")
#     test_file = test_path_parts[0]       # e.g., "examples/test_simple_login.py"
#     # test_file.split("/")[1]            # e.g., "test_simple_login.py"
#     test_name = test_path_parts[1]       # e.g., "test_logo"
#
#     # Construct the desired path structure
#     screenshot_filename = f"{test_file.split("/")[1]}_{test_name}.png".replace("/", "_").replace("\\", "_")
#     screenshot_path = os.path.join("reports", test_file.split('/')[0], screenshot_filename)
#
#     os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)  # Ensure the directory exists
#     driver.save_screenshot(screenshot_path)
#     # TODO logging.info(f"Screenshot saved at: {file_path}")
#     return screenshot_path  # Return for debugging/logging


def generate_random_email(char_len=5, prefix="", suffix="@mail.com") -> str:
    """Generate a random email address with random chars and digits."""
    random_str = ""
    for _ in range(char_len):
        random_str += random.choice(string.ascii_lowercase + string.digits)

    email = prefix + random_str + suffix
    return email
