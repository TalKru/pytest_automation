# ---------------------------------------------------------------------
# locator_tuple = (By.ID, 'start-date')
# element = wait.until(EC.element_to_be_clickable(locator_tuple))
# ActionChains(driver).move_to_element(element).click().perform()
# ---------------------------------------------------------------------
# element = driver.find_element(By.ID, 'start-date')
# element.click()
# ---------------------------------------------------------------------
from pytest_metadata.plugin import metadata_key

import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys
import time
from datetime import datetime
import os


@pytest.fixture(scope="function")
def driver() -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--ignore-certificate-errors")
    # chrome_options.add_argument("--incognito")  # will mess up file downloads
    # chrome_options.add_argument("--headless=new")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def wait(driver, wait_time_sec=10) -> WebDriverWait:
    wait = WebDriverWait(driver, wait_time_sec, poll_frequency=1, ignored_exceptions=[])
    # driver.implicitly_wait(WAIT_TIME_SEC)
    return wait


# ==============================[Add test suite name and test tame for each logger]=================================
# def get_test_context(request) -> str:
#     """
#     Returns a string with the test context (test file and test case name)
#     based on the request.node.nodeid.
#     Example output: "tests_test_example_py_test_login"
#     """
#     return request.node.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")

def get_test_context(request) -> str:
    """
    Returns a string with the test context based on request.node.nodeid.
    For example, if request.node.nodeid is:
      "tests/test_01_account_registration.py::test_correct_account_registration[2-2]"
    this function will return:
      "01_account_registration_correct_account_registration[2-2]"
    It removes "tests_test_" and ".py_test_" prefixes.
    """
    # Replace separators with underscores.
    context = request.node.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
    # Remove unwanted prefixes (assuming a typical pattern).
    if context.startswith("tests_test_"):
        context = context[len("tests_test_"):]
    context = context.replace(".py_test_", "_")
    return context


@pytest.fixture
def test_context(request):
    """Fixture to provide test context for logging purposes."""
    return get_test_context(request)


# ==============================[embed screenshot in html report]=================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook that is called after each test phase (setup, call, teardown).
    This hook attaches a screenshot to the HTML report if a test fails.
    It assumes that screenshots are saved in the project root folder "screenshots".
    The relative path from the HTML report (assumed to be in the "reports" folder) to the
    screenshots folder is "../screenshots".
    """
    # Get the pytest-html plugin instance.
    pytest_html = item.config.pluginmanager.getplugin('html')

    # Yield to let the test run and capture its report.
    outcome = yield
    report = outcome.get_result()

    # Retrieve any existing extra information for the report.
    extra = getattr(report, 'extra', [])

    # Process only during the 'call' or 'setup' phase.
    if report.when in ('call', 'setup'):
        xfail = hasattr(report, 'wasxfail')
        # Attach screenshot if test failed (and wasn't expected to fail) or if skipped but expected to fail.
        if (report.failed and not xfail) or (report.skipped and xfail):
            # Build the screenshot filename exactly as in capture_screenshot().
            screenshot_filename = f"{report.nodeid.replace('::', '_').replace('/', '_').replace('\\', '_')}.png"
            # Define the relative path from the HTML report location (e.g., reports/report.html)
            # to the screenshots folder at the project root.
            relative_path = os.path.join("..", "screenshots", screenshot_filename)

            # Create an HTML snippet to embed the screenshot in the report.
            html = (
                f'<div><img src="{relative_path}" alt="screenshot" '
                'style="width:304px;height:228px;" onclick="window.open(this.src)" align="right"/></div>'
            )
            extra.append(pytest_html.extras.html(html))

    # Set the extra info back on the report.
    report.extra = extra

# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     now = datetime.now()
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, 'extra', [])
#     if report.when == 'call' or report.when == "setup":
#         xfail = hasattr(report, 'wasxfail')
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             file_name = report.nodeid.replace("::", "_") + ".png"
#             # file_name = "screenshot" + now.strftime("%S%H%d%m%Y") + ".png"
#             # driver.get_screenshot_as_file(file_name)
#             if file_name:
#                 html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
#                        'onclick="window.open(this.src)" align="right"/></div>' % file_name
#                 extra.append(pytest_html.extras.html(html))
#         report.extra = extra


# @pytest.hookimpl(tryfirst=True)
# def pytest_configure(config):
#     now = datetime.now()
#     report_dir = os.path.join('reports', now.strftime("%S%H%d%m%Y"))
#     report_dir.mkdir(parents=True, exist_ok=True)
#     pytest_html = report_dir / f"report_{now.strftime('%H%M%S')}.html"
#     config.option.htmlpath = pytest_html
#     config.option.self_contained_html = True


# ============================[modify report metadata]=====================================
@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    """ remove data fields from the report opening"""
    metadata.pop("Plugins", None)
    metadata.pop("Platform", None)
    metadata.pop("Python", None)


def pytest_configure(config):
    """ add meta-data fields to the report opening """
    config.stash[metadata_key]["TITLE_TEXT_1"] = 'pytest_configure()_EDIT_YOUR_TEXT'
    config.stash[metadata_key]["TITLE_TEXT_2"] = 'pytest_configure()_EDIT_YOUR_TEXT'
    config.stash[metadata_key]["TITLE_TEXT_3"] = 'pytest_configure()_EDIT_YOUR_TEXT'


def pytest_html_report_title(report):
    """ edit the main Title """
    report.title = "Pytest HTML Automation Report (TAL)"
# ============================[modify report metadata]=====================================



