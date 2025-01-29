import pytest


class TestClass:
    """
    The decorator specify the input arguments for the test
    and a list of tuples when each tuple (...) contains the values for the test.
    The test will be invoked for the amount of tuples in the list
    NOTE: the parameters names 'x, y' must match the names in the decorator 'x, y'
    """
    @pytest.mark.parametrize('x, y', [(1, 1), (3, 5), (10, 10), (5, 20)])  # 4 tests will run
    def test_if_equal(self, x, y):
        assert x == y

    @pytest.mark.parametrize('a, b, c', [(1, 1, 2), (2, 3, 5), (1, 1, 99), (3, 4, 7), (0, 0, 0)])  # 5 tests will run
    def test_calculation(self, a, b, c):
        assert a + b == c
