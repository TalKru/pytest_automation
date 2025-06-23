# ---------------------------------------------------------------------------------------------------------- #
import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys
from pytest_metadata.plugin import metadata_key
# ---------------------------------------------------------------------------------------------------------- #
import time
from datetime import datetime
import os
# ---------------------------------------------------------------------------------------------------------- #


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


# wait encapsulates your explicit-wait policy (timeout, polling interval, ignored exceptions)
# driver.implicitly_wait(WAIT_TIME_SEC)
@pytest.fixture(scope="function")
def wait(driver, wait_time_sec=10) -> WebDriverWait:
    wait = WebDriverWait(driver, wait_time_sec, poll_frequency=1, ignored_exceptions=[])
    return wait


# ==============================[Add test suite/name/iteration for each log msg]=================================
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
    Since the HTML report is generated in a subfolder inside "reports" (for example, a daily folder),
    we need to go up two levels to reference the screenshots folder:
        <project_root>/reports/DATE/<report.html>  --> Relative path: ../../screenshots/<filename>
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

            # Calculate the relative path from the report file to the screenshots folder.
            # Assuming the report is in: <project_root>/reports/DATE/report.html,
            # to get to <project_root>/screenshots, we need to go up two levels:
            relative_path = os.path.join("..", "..", "screenshots", screenshot_filename)
            #relative_path = os.path.join("..", "screenshots", screenshot_filename) # Define the relative path from the HTML report location (e.g., reports/report.html) to the screenshots folder at the project root.

            # Create an HTML snippet to embed the screenshot in the report.
            html = (
                f'<div><img src="{relative_path}" alt="screenshot" '
                'style="width:304px;height:228px;" onclick="window.open(this.src)" align="right"/></div>'
            )
            extra.append(pytest_html.extras.html(html))

    # Set the extra info back on the report.
    report.extras = extra  # report.extra = extra  # attribute is deprecated?


# ============================[Set HTML Report Path and modify report metadata]=====================================
@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    """ remove data fields from the report opening"""
    metadata.pop("Plugins", None)
    metadata.pop("Platform", None)
    metadata.pop("Python", None)


def pytest_html_report_title(report):
    """ edit the main Title """
    report.title = "Pytest-HTML Automation Report (TAL)"

# NOTE: conflict issue, currently not working!
# will work only the other pytest_configure() will be removed
# def pytest_configure(config):
#     # adds meta-data fields to the report opening
#     config._metadata["TITLE_TEXT_1"] = 'EDIT_YOUR_TEXT'
#     config._metadata["TITLE_TEXT_2"] = 'EDIT_YOUR_TEXT'
#     config._metadata["TITLE_TEXT_3"] = 'EDIT_YOUR_TEXT'


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """
    Configures the HTML report location and adds custom metadata to the report.
    This hook:
    1. Creates a "reports" folder in the project root if it doesn't exist.
    2. Creates a subfolder for the current day using the format YYYY-MM-DD.
    3. Sets config.option.htmlpath to a file in that daily folder with a timestamp in its filename.
    """
    # Base reports folder (project_root/reports)
    base_reports_dir = os.path.join(os.path.abspath(os.curdir), "reports")
    os.makedirs(base_reports_dir, exist_ok=True)

    # Create a subfolder for the current day (YYYY-MM-DD)
    today_folder = datetime.now().strftime("%Y-%m-%d")
    daily_reports_dir = os.path.join(base_reports_dir, today_folder)
    os.makedirs(daily_reports_dir, exist_ok=True)

    # Create a timestamped filename for the HTML report, e.g. "09-02-2025 13-28-51.html"
    timestamp = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    html_report_file = os.path.join(daily_reports_dir, f"{timestamp}.html")

    # Set the HTML report path.
    config.option.htmlpath = html_report_file


# ---------------------------------------------------------------------
# locator_tuple = (By.ID, 'start-date')
# element = wait.until(EC.element_to_be_clickable(locator_tuple))
# ActionChains(driver).move_to_element(element).click().perform()
# ---------------------------------------------------------------------
# element = driver.find_element(By.ID, 'start-date')
# element.click()
# ---------------------------------------------------------------------


# ============================[older versions, might be usful for debug]=====================================

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

# ==============================[Add test suite name and test tame for each logger]=================================
# def get_test_context(request) -> str:
#     """
#     Returns a string with the test context (test file and test case name)
#     based on the request.node.nodeid.
#     Example output: "tests_test_example_py_test_login"
#     """
#     return request.node.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
