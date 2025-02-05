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


# ===============================================================================================
# special pytest config func, getting browser param value
# This will get the value from terminal
# and it will allow to add argument to the command line:

# pytest -s .\examples\test_[YOUR-TEST] --browser chrome --html=reports\report.html
# pytest -s .\examples\test_[YOUR-TEST] --browser edge --html=reports\report.html
# pytest -s .\examples\test_[YOUR-TEST] --browser firefox --html=reports\report.html

# later, those values chrome, edge... will be received by the driver fixture...
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to use for tests")
# ===============================================================================================


# passing browser param value to driver fixture
@pytest.fixture(scope="function")
def browser(request):  # This will return the Browser value to driver setup method
    return request.config.getoption("--browser")
# ===============================================================================================


@pytest.fixture(scope="function")
def driver(browser) -> webdriver:
    """
    :param browser: passed ONLY as terminal FLAG
    for it work correctly, when executing the test that using this conftest file,
    add the flag --browser to the pytest terminal command:
    [ pytest -s .\tests_PATH\test_FILE.py --browser chrome ]
    """
    if browser == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--incognito")  # will mess up file downloads
        # chrome_options.add_argument("--headless=new")
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=chrome_options)
        yield driver
        driver.quit()

    elif browser == 'edge':
        options = webdriver.EdgeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        driver = webdriver.Edge(options=options)
        yield driver
        driver.quit()

    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        yield driver
        driver.quit()


@pytest.fixture(scope="function")
def wait(driver, wait_time_sec=10) -> WebDriverWait:
    wait = WebDriverWait(driver, wait_time_sec, poll_frequency=1, ignored_exceptions=[])
    # driver.implicitly_wait(WAIT_TIME_SEC)
    return wait


#==============================[embed screenshot in html report]=================================

# @pytest.hookimpl(tryfirst=True)
# def pytest_configure(config):
#     now = datetime.now()
#     report_dir = os.path.join('reports', now.strftime("%S%H%d%m%Y"))
#     report_dir.mkdir(parents=True, exist_ok=True)
#     pytest_html = report_dir / f"report_{now.strftime('%H%M%S')}.html"
#     config.option.htmlpath = pytest_html
#     config.option.self_contained_html = True



# ============================[modify report metadata]=====================================
@pytest.mark.optionalhook
def pytest_metadata(metadata):
    """ remove data """
    metadata.pop("Plugins", None)
    metadata.pop("Platform", None)
    metadata.pop("Python", None)

def pytest_configure(config):
    """ add data fields """
    config.stash[metadata_key]["Project"] = '~~~~@#@#@#@#@~~~~'
    config.stash[metadata_key]["Module"] = '~~~~@#@#@#@#@~~~~'
    config.stash[metadata_key]["Project"] = '~~~~@#@#@#@#@~~~~'

def pytest_html_report_title(report):
    """ edit the main Title """
    report.title = "Pytest HTML Automation Report (TAL)"
# ============================[modify report metadata]=====================================