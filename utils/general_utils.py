
from selenium import webdriver
import random
import string
import os
from utils.logger import logger
from tests.conftest import SCREENSHOTS_DIR


def capture_screenshot(driver: webdriver, request) -> str:
    """
    Capture into SCREENSHOTS_DIR, using the pytest nodeid for filename.
    """
    # Ensure the screenshots folder exists
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    # Build a safe filename from the pytest nodeid
    filename = request.node.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_") + ".png"
    file_path = os.path.join(SCREENSHOTS_DIR, filename)

    driver.save_screenshot(file_path)
    logger.warning(f"Screenshot saved at: {file_path}")
    # Coerce to str so the return type exactly matches the annotation
    return str(file_path)


# def capture_screenshot(driver: webdriver, request):
#     """
#     Capture a screenshot and save it using the test's node ID for naming.
#     Screenshots are saved in the absolute path:
#         <project_root>/screenshots/<screenshot_filename>
#     The filename is built from the test's nodeid (with characters like '::' and '/' replaced
#     with underscores), ensuring a unique and valid filename on all OSes.
#     """
#     # Build a unique screenshot filename from the test's node id.
#     # request.node.nodeid returns something like "tests/test_example.py::test_logo"
#     # We replace '::' and '/' with '_' to form a valid filename.
#     screenshot_filename = f"{request.node.nodeid.replace('::', '_').replace('/', '_').replace('\\', '_')}.png"
#
#     # Define the absolute path to the screenshots folder.
#     # os.getcwd() returns the current working directory (the project root)
#     screenshots_dir = os.path.join(os.getcwd(), "screenshots")
#
#     # Create the screenshots folder if it does not exist.
#     os.makedirs(screenshots_dir, exist_ok=True)
#
#     # Construct the full path for the screenshot file.
#     screenshot_path = os.path.join(screenshots_dir, screenshot_filename)
#
#     # Capture the screenshot using the Selenium WebDriver.
#     driver.save_screenshot(screenshot_path)
#     logger.warning(f"Screenshot saved at: {file_path}")
#     return screenshot_path  # Return the path for logging or debugging.


def generate_random_email(char_len=5, prefix="", suffix="@mail.com") -> str:
    """Generate a random email address with random chars and digits."""
    random_str = ""
    for _ in range(char_len):
        random_str += random.choice(string.ascii_lowercase + string.digits)

    email = prefix + random_str + suffix
    return email
