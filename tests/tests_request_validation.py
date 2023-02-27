from pydantic.error_wrappers import ValidationError

from app.schemas import RequestModel


def test_validate_request_successfully():
    data = {"department": "01", "surface": "40", "maximum_rent_price": "300"}

    req = RequestModel(**data)
    assert req.department == data["department"]
    assert req.surface == 40
    assert req.maximum_rent_price == 300.0


def test_validate_request_failed():
    data = {"department": "01", "surface": "-30", "maximum_rent_price": "300"}
    try:
        RequestModel(**data)
        assert False, "Shouldn't arrive here"
    except ValidationError:
        assert True

    data = {"surface": "-30", "maximum_rent_price": "300"}
    try:
        RequestModel(**data)
        assert False, "Shouldn't arrive here"
    except ValidationError:
        assert True
