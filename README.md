
project_root/
├── tests/                # Contains all test cases
│   ├── conftest.py       # Pytest fixtures and hooks
│   ├── test_login.py     # Example test file
│   └── test_product_page.py # Another example test file
├── pages/                # Page Object Model (POM) classes
│   ├── login_page.py
│   └── product_page.py
├── utils/                # Utility functions and helper classes
│   ├── config.py         # Configuration settings
│   ├── locators.py       # Element locators (if not in POM)
│   ├── logger.py         # Logging setup
│   └── webdriver_manager.py # Manages WebDriver instances
├── data/                 # Test data (e.g., CSV, JSON files)
│   └── test_data.csv
├── reports/              # Test reports (e.g., HTML reports)
├── requirements.txt      # Project dependencies
├── pytest.ini            # Pytest configuration
├── README.md             # Project documentation
└── .gitignore

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

========================================================[NOTES]========================================================
to skip a test, use a marker:
[ @pytest.mark.skip ]
========================================================[NOTES]========================================================
when creating a fixture, set the scope accordingly to the needs and lifecycle, the default scope is "function"
[ @pytest.fixture(scope="function") ]

The scope="module" argument means the fixture will run only once per module (file), 
not for every test function. Other scopes include:
"function" (default): Runs for each test function.
"class": Runs once per test class.
"package": Runs once per package of tests.
"session": Runs once per test session.
========================================================[NOTES]========================================================
parallel execution capabilities (via the pytest-xdist plugin)
install: [ pip install pytest-xdist ]
Run:     [ pytest -n NUM ... ] (where NUM is the number of parallel processes you want to use). 
For example, pytest -n 4 will run your tests using 4 processes.
========================================================[NOTES]========================================================

========================================================[NOTES]========================================================

========================================================[NOTES]========================================================

========================================================[NOTES]========================================================

========================================================[NOTES]========================================================