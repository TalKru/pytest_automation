import pytest


class TestSignup:

    @pytest.mark.skip  # <---- skip this test!
    def test_SignupByEmail(self, setup):
        print("This is signup by email..")
        assert True

    @pytest.mark.skip  # <---- skip this test!
    def test_SignupFacebook(self, setup):
        print("This is signup by facebook..")
        assert True

    def test_SignupTwitter(self, setup):
        print("This is signup by twitter..")
        assert True
