"""
run in terminal with:
pytest -v -s .\tests\test_example_3.py
"""
import pytest


class TestClass:
    # fixture example, should be in a separate file named conftests
    @pytest.fixture(scope="function")
    def setup(self):
        # steps that will execute BEFORE each test
        print("step 1: launch browser")
        print("step 2: open app")

        yield  # return + pause

        # steps will execute AFTER each test
        print("step 999: closing browser!")

    def test_login(self, setup):
        print('test_login...')
        assert True == True

    def test_search(self, setup):
        print('test_search...')
        assert False == False

    def test_logout(self, setup):
        print('test_logout...')
        assert 13 is 7



