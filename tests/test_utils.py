from app.utils.city_informations import CityInfosService

"""
These tests have been written in order to show the importance of testing
The services classes and functions that we write for the project
As it's just a test, I preferred not to mock the responses we could get
from these services. But It should be done by mocking apis.
"""


def test_assert_resultNone_for_non_existing_ratings():
    res = CityInfosService.retrieve_city_rating("La roche-guyon")
    assert res is None


def test_assert_resultNone_for_exusting_ratings():
    res = CityInfosService.retrieve_city_rating("Bezons")
    assert res is not None and type(res) == float
