
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
# ---------------------------------------------------------------------------------------------------------- #
import os
from pathlib import Path
# resolve project root as a string once
ROOT_DIR = str(Path(__file__).parent.parent.resolve())

# define the others as strings built off ROOT_DIR
SCREENSHOTS_DIR  = f"{ROOT_DIR}/screenshots"
REPORTS_BASE_DIR = f"{ROOT_DIR}/reports"
LOGS_DIR         = f"{ROOT_DIR}/logs"


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
    Attach screenshot to pytest-html report on failure.
    We save all screenshots under SCREENSHOTS_DIR.
    We compute a correct relative path from the HTML file's folder
    (item.config.option.htmlpath) back to SCREENSHOTS_DIR.
    """
    # get an active instance of the pytest-html plugin.
    # This allows us to use its specific helper functions.
    html_plugin = item.config.pluginmanager.getplugin("html")

    # 'yield' allows us to wait for the test to finish and then
    # inspect its result to decide if we need to take further action as a screenshot to the report.
    outcome = yield

    # We get the standard 'report' object from the 'outcome' object.
    # 'report' object contains all the info about test result (passed, failed, name, duration...)
    report = outcome.get_result()

    # 'report.extra' is a list used by pytest-html to store extra content
    # (like images or links) for a test's row in the HTML report.
    # 'getattr(report, "extra", [])' safely gets this list if it exists,
    extra = getattr(report, "extra", [])

    # add screenshots only for failures that happen during test's 'setup' phase or the 'call' phase
    # (the actual 'test_...' function fails). We ignore the 'teardown' phase.
    if report.when in ("call", "setup"):

        # This boolean flag checks if the test truly failed. 'report.failed' is True for a failure.
        # 'not hasattr(report, "wasxfail")' ensures this isn't a test that was *expected* to fail.
        failed: bool = report.failed and not hasattr(report, "wasxfail")

        # This flag checks if a test marked as 'xfail' was skipped.
        skipped: bool = report.skipped and hasattr(report, "wasxfail")
        if failed or skipped:
            # 1) screenshot filename as per capture_screenshot()
            filename = (
                    report.nodeid
                    .replace("::", "_")
                    .replace("/", "_")
                    .replace("\\", "_")
                    .replace("test_", "")
                    .replace("tests_", "")
                    .replace(".py", "")
                    + ".png"
            )
            # 3) where the report HTML lives
            html_path = item.config.option.htmlpath

            # 4) compute relative from report folder back to screenshots
            report_dir     = os.path.dirname(html_path)
            rel_to_reports = os.path.relpath(SCREENSHOTS_DIR, report_dir)
            rel_img_path   = os.path.join(rel_to_reports, filename)

            # 5) Generate the HTML snippet for the screenshot image
            img_html = (
                f'<div>'
                f'  <img src="{rel_img_path}"'
                f'       alt="screenshot"'
                f'       style="width:304px;height:228px;"'
                f'       onclick="window.open(this.src)"'
                f'       align="right"/>'
                f'</div>'
            )
            # Add the HTML snippet to the report's 'extra' content
            extra.append(html_plugin.extras.html(img_html))
    # Assign modified 'extra' list back to the report object to ensures it gets included in the HTML file.
    report.extra = extra


# ============================[Set HTML Report Path and modify report metadata]=====================================
@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    """ remove data fields from the report opening"""
    # metadata.pop("Plugins", None)
    # metadata.pop("Python", None)
    metadata.pop("Platform", None)                                  # remove metadata
    metadata.pop("JAVA_HOME", None)                                 # remove metadata
    metadata['Project'] = 'My Awesome Automation project (Tal K.)'  # add metadata


def pytest_html_report_title(report):
    """ edit the main Title """
    report.title = "QA Automation Report (TAL)"


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """
    Configures the HTML report location and adds custom metadata to the report.
    This hook:
    1. Creates a "reports" folder in the project root if it doesn't exist.
    2. Creates a subfolder for the current day using the format YYYY-MM-DD.
    3. Sets config.option.htmlpath to a file in that daily folder with a timestamp in its filename.
    """
    base_reports_dir = REPORTS_BASE_DIR  # Base reports folder (always use our project root)

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



# ============================[examples]=====================================
"""
@pytest.fixture
def request():
    # Provides:
    # - `nodeid`: the full test identifier (e.g., "tests/test_example.py::test_example").
    # - `addfinalizer(func)`: a no-op stub showing where teardown hooks could be registered.
    ...
    return DummyRequest(nodeid="tests/test_example.py::test_example")

@pytest.fixture(scope="session")
def config():
    # Load URLs, credentials, timeouts from a config file or env vars.
    return {
        "base_url": os.getenv("BASE_URL", "https://myapp.example.com"),
        "api_token": os.getenv("API_TOKEN", "secret"),
        "timeout": 10
    }

@pytest.fixture(scope="session")
def api_client(config):
    # A simple HTTP client configured with your API token.
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {config['api_token']}"})
    yield session
    session.close()
"""