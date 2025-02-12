# **Python automation testing project.**
### ***With Selenium, Pytest, HTML reports, Screenshots & logs.***

![Project Theme](examples/projectTheme.png)
```
pytest_automation/ 
├── configurations/ 
│   └── config.ini  
├── examples/       
├── logs/                       
├── pages/               
│   ├── __init__.py       
│   ├── home_page.py            
│   ├── login_page.py          
│   └── register_page.py 
├── reports/              
├── screenshots/          
├── tests/                
│   ├── __init__.py             
│   ├── conftest.py       
│   └── test_01.py         
├── utils/                 
│   ├── __init__.py             
│   ├── excel_utils.py         
│   ├── general_utils.py       
│   ├── logger.py           
│   └── read_config_data.py    
├── .gitignore               
├── pytest.ini             
├── README.md              
└── requirements.txt       
```

Explanation of Key Components:

tests/: This directory houses all your test cases. Each file (e.g., test_login.py) contains one or more test functions.
conftest.py: This file is crucial for Pytest. It contains fixtures (setup and teardown methods) and hooks 
that are shared across multiple test files.
pages/: This directory implements the Page Object Model (POM). Each file represents a web page and contains methods for 
interacting with the elements on that page. This promotes code reusability and makes tests easier to maintain.
utils/: This directory contains utility functions and helper classes that are used throughout the project.
config.py: Stores configuration settings like URLs, browser types, and timeouts.
locators.py: (Optional) If you're not putting locators in your POM classes, you can store them here.
logger.py: Sets up logging for your tests.
webdriver_manager.py: Manages the WebDriver instances (e.g., ChromeDriver, GeckoDriver).
data/: This directory stores test data, such as CSV or JSON files, that your tests might use.
reports/: This directory will contain the generated test reports after running your tests.
requirements.txt: This file lists all the project's dependencies (e.g., selenium, pytest). You can install them using 
pip install -r requirements.txt.
pytest.ini: This file contains Pytest configuration settings, such as markers, plugins, and report format.
README.md: This file provides a description of the project and instructions on how to run the tests.


Explanation of Key Libraries
pytest
The main testing framework for writing and running tests.

pytest-html
Generates detailed HTML reports for your test runs.

pytest-xdist
Enables parallel test execution, speeding up large test suites.

pytest-rerunfailures
Reruns failed tests automatically to handle flakiness in test environments.

pytest-mock
Simplifies mocking objects and functions in your tests.

selenium
For browser automation, commonly used with UI testing.

requests
Helpful for testing APIs or integrating web-based operations.

jsonschema
For validating JSON responses from APIs against expected schemas.

webdriver-manager
Automatically downloads and configures browser drivers for Selenium.

pandas
Useful for handling test data in CSV, Excel, or other structured formats.

Faker
Generates fake data for testing (e.g., names, addresses, emails).

loguru
Adds better logging capabilities, making it easier to debug your tests.

========================================================(Notes)========================================================<br/>
to skip a test, use a marker:
```
@pytest.mark.skip
```
========================================================(Notes)========================================================<br/>
when creating a fixture, set the scope accordingly to the needs and lifecycle, the default scope is "function"
```
@pytest.fixture(scope="function")
@pytest.fixture(scope="class")
@pytest.fixture(scope="package")
@pytest.fixture(scope="session")
```
The scope="module" argument means the fixture will run only once per module (file), 
not for every test function. Other scopes include:
"function" (default): Runs for each test function.
"class": Runs once per test class.
"package": Runs once per package of tests.
"session": Runs once per test session.

========================================================(Notes)========================================================<br/>
parallel execution capabilities (via the pytest-xdist plugin)
```
$: pip install pytest-xdist
```
Run:     
```
pytest -n NUM ...
```
(where NUM is the number of parallel processes you want to use). 
For example, pytest ```-n 4``` will run your tests using 4 processes.
========================================================(Notes)========================================================<br/>
If you want to create a requirements.txt file from your currently installed packages, use:
```
$: pip freeze > root\requirements.txt
```
========================================================(Notes)========================================================<br/>
install correctly the modules from requirements.txt
```
$: pip install --upgrade -r root\requirements.txt
```
========================================================(Notes)========================================================<br/>
How to run all the test files (all test cases that isn't marked with a .skip marker)
```
$: pytest .\tests\
```
with the current setup, no need to specify the flags as -v -s -n=3 can be configured inside 
\pytest_automation\pytest.ini file to execute automatically,
also, no need to specify the html test creation flag (--html=reports\report.html) 
since pytest will use pytest_configure(config) function from conftest.py file,
this function configures the location and naming scheme of the generated log files.
========================================================(Notes)========================================================<br/>
1. Define Custom Markers in Your Tests:
In your test files, use the @pytest.mark decorator with a custom name such as sanity, regression, etc.
```
@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.smoke
```

2. Register the Markers in pytest.ini:
register your custom markers in your pytest.ini file. This avoids warnings and makes your markers discoverable.
Create (or update) your root\pytest.ini with the following:
```
[pytest]
markers =
    sanity: marks tests as sanity tests.
    regression: marks tests as regression tests.
    smoke: marks tests as smoke tests.

```
3. Run Tests by Marker:
You can then execute only the tests for a specific group using the ```-m``` flag.
To run sanity tests:
```
pytest -m "sanity"
```
To run regression tests:
```
pytest -m "regression"
```
You can also combine markers. For example, to run both sanity and smoke tests:
```
pytest -m "sanity or smoke"
```
Or to run tests that are both regression and smoke (if applicable):
```
pytest -m "regression and smoke"
```
========================================================(Notes)========================================================<br/>

========================================================(Notes)========================================================<br/>

========================================================(Notes)========================================================<br/>