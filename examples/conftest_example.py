import pytest


@pytest.fixture(scope="function")  # decorator
def setup():
    print("Launching browser...")  # Executes once before every test method
    yield
    print("closing browser..")  # Executes Once after every test method
