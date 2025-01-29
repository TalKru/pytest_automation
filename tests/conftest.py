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


@pytest.fixture(scope="function")
def driver() -> webdriver:
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


@pytest.fixture(scope="function")
def wait(driver, wait_time_sec=10) -> WebDriverWait:
    wait = WebDriverWait(driver, wait_time_sec, poll_frequency=1, ignored_exceptions=[])
    # driver.implicitly_wait(WAIT_TIME_SEC)
    return wait


# ==============================[embed screenshot in html report]=================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    now = datetime.now()
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            # file_name = "screenshot" + now.strftime("%S%H%d%m%Y") + ".png"
            # driver.get_screenshot_as_file(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


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



