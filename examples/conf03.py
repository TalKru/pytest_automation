
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
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

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()



@pytest.fixture(scope="function")
def wait(driver, wait_time_sec=10) -> WebDriverWait:
    wait = WebDriverWait(driver, wait_time_sec, poll_frequency=1, ignored_exceptions=[])
    return wait


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
    # grab the html plugin
    html_plugin = item.config.pluginmanager.getplugin("html")

    # run the test and get the report object
    outcome = yield
    report  = outcome.get_result()
    extra   = getattr(report, "extra", [])

    # only add on actual test call or setup failure
    if report.when in ("call", "setup"):
        failed  = report.failed and not hasattr(report, "wasxfail")
        skipped = report.skipped and hasattr(report, "wasxfail")
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

            # 5) generate the <img> tag
            img_html = (
                f'<div>'
                f'  <img src="{rel_img_path}"'
                f'       alt="screenshot"'
                f'       style="width:304px;height:228px;"'
                f'       onclick="window.open(this.src)"'
                f'       align="right"/>'
                f'</div>'
            )
            extra.append(html_plugin.extras.html(img_html))

    report.extra = extra


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Attach screenshot to pytest-html report on failure.
    We save all screenshots under SCREENSHOTS_DIR.
    We compute a correct relative path from the HTML file's folder
    (item.config.option.htmlpath) back to SCREENSHOTS_DIR.
    """
    # This line gets an active instance of the pytest-html plugin.
    # This allows us to use its specific helper functions if needed,
    # such as 'extras.html()' which ensures HTML is treated as raw HTML
    # instead of plain text.
    html_plugin = item.config.pluginmanager.getplugin("html")

    # ==================== The `yield` Keyword Explained ====================
    # The '@pytest.hookimpl(hookwrapper=True)' decorator turns this function
    # into a special generator that "wraps" around pytest's own test execution process.
    # The 'yield' statement is the central point of this wrapper.
    #
    # 1. Code BEFORE yield: This code runs before pytest proceeds with running
    #    the test and creating the report.
    #
    # 2. The 'yield' itself: This statement pauses this function and passes
    #    control back to pytest. Pytest then continues its process, which includes
    #    running the test function and generating the initial test report.
    #
    # 3. Code AFTER yield: This code resumes execution ONLY AFTER the test
    #    has finished and the report has been created. The 'yield' keyword
    #    returns an 'outcome' object, which contains the results of the test.
    #
    # In short, 'yield' allows us to wait for the test to finish and then
    # inspect its result to decide if we need to take further action, like
    # adding a screenshot to the report.
    # ======================================================================
    outcome = yield

    # We get the standard 'report' object from the 'outcome' object.
    # The 'report' object contains all the information about the test result,
    # such as whether it passed, failed, its name, duration, etc.
    report = outcome.get_result()

    # 'report.extra' is a list used by pytest-html to store extra content
    # (like images or links) for a test's row in the HTML report.
    # 'getattr(report, "extra", [])' safely gets this list if it exists,
    # or creates a new empty list if it doesn't.
    extra = getattr(report, "extra", [])

    # We only want to add screenshots for failures that happen during the
    # test's 'setup' phase (e.g., a fixture fails) or the 'call' phase
    # (the actual 'test_...' function fails). We ignore the 'teardown' phase.
    if report.when in ("call", "setup"):

        # This boolean flag checks if the test truly failed.
        # 'report.failed' is True for a failure.
        # 'not hasattr(report, "wasxfail")' ensures this isn't a test
        # that was *expected* to fail (marked with @pytest.mark.xfail).
        failed = report.failed and not hasattr(report, "wasxfail")

        # This boolean flag checks if a test marked as 'xfail' was skipped.
        # This can sometimes be a condition you want to capture.
        skipped = report.skipped and hasattr(report, "wasxfail")

        # If the test either failed or was an xfail-skip, we proceed to add the screenshot.
        if failed or skipped:
            # --- Step 1: Generate a unique filename for the screenshot ---
            # 'report.nodeid' is the unique ID of the test (e.g., "tests/test_login.py::test_valid_login").
            # This block of '.replace()' calls cleans up the nodeid to make it a valid
            # and more readable filename (e.g., "login_valid_login.png").
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

            # --- Step 2: Get the path to the final HTML report ---
            # 'item.config.option.htmlpath' retrieves the full path where the report
            # will be saved (e.g., "C:/project/reports/2025-06-25/report.html").
            # This path is set by the --html command-line option.
            html_path = item.config.option.htmlpath

            # --- Step 3: Calculate the relative path from the report to the screenshot ---
            # This is a crucial step. The <img> tag in the HTML report needs a relative
            # path to find the image file.

            # First, get the directory where the HTML report itself will be located.
            report_dir = os.path.dirname(html_path)

            # Next, calculate the relative path from that report directory to your
            # main screenshots folder (SCREENSHOTS_DIR).
            rel_to_reports = os.path.relpath(SCREENSHOTS_DIR, report_dir)

            # Finally, join the relative directory path with the specific screenshot filename.
            # This gives us the final value for the 'src' attribute in the <img> tag.
            rel_img_path = os.path.join(rel_to_reports, filename)

            # --- Step 4: Generate the HTML snippet for the screenshot image ---
            # We create an HTML string for a clickable image thumbnail.
            img_html = (
                f'<div>'  # A container for the image.
                f'  <img src="{rel_img_path}"'  # The 'src' attribute points to our image file.
                f'       alt="screenshot"'  # Alt text for accessibility.
                f'       style="width:304px;height:228px;"'  # Inline style to set the thumbnail size.
                f'       onclick="window.open(this.src)"'  # JavaScript to open the full image in a new tab when clicked.
                f'       align="right"/>'  # Aligns the image to the right of the cell.
                f'</div>'
            )

            # --- Step 5: Add the HTML snippet to the report's 'extra' content ---
            # We append our generated HTML to the 'extra' list.
            # 'html_plugin.extras.html()' wraps our string in a special object
            # to ensure pytest-html renders it as raw HTML.
            extra.append(html_plugin.extras.html(img_html))

    # Assign modified 'extra' list back to the report object to ensures it gets included in the HTML file.
    report.extra = extra


@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    """ remove data fields from the report opening"""
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

