import pytest


class TestClass:
    """
    every following test depends on this test to pass
    if this test will fail, there is no need to follow other tests
    to save times a resources
    """
    @pytest.mark.dependency()
    def test_openApp(self):
        assert False  # <--- make it fail!

    @pytest.mark.dependency(depends=['TestClass::test_openApp'])
    def test_login(self):
        assert True

    @pytest.mark.dependency(depends=['TestClass::test_login'])
    def test_search(self):
        assert True

    # NOTE: one test may be dependent on several other
    @pytest.mark.dependency(depends=['TestClass::test_login', 'TestClass::test_search'])
    def test_advsearch(self):
        assert True

    @pytest.mark.dependency(depends=['TestClass::test_login'])
    def test_logout(self):
        assert True