"""
run in terminal with:
pytest -v -s .\tests\test_example_2.py
"""
import pytest


class TestClass:
    # ==============================================================
    # pytest will not consider this method as test
    # as it is not containing "test" in the name.
    # will execute before the test methods.
    @pytest.fixture(scope="function")
    def setup(self):
        print("step 1: launch browser")
        print("step 2: open app")

    @pytest.fixture(scope="function")
    def additional_steps(self):
        print("step 3: special configs")
    # ==============================================================

    def test_login(self, setup):
        print('test_login...')
        assert True

    # NOTE: only this method used the fixture "additional_steps()"
    # as it may need more functionality for a specific test case
    def test_search(self, setup, additional_steps):
        print('test_search...')
        assert False

    def test_logout(self, setup):
        print('test_logout...')
        assert 13 is 7



