from typing import List

from pydantic import BaseModel, PositiveFloat, PositiveInt


class RequestModel(BaseModel):
    department: str
    surface: PositiveInt
    maximum_rent_price: PositiveFloat


class ZipCodeModel(BaseModel):
    zipcode: str

    class Config:
        orm_mode = True


class CityModel(BaseModel):
    name: str
    rating: float
    zipcodes: List[ZipCodeModel]

    class Config:
        orm_mode = True


class IndicatorModel(BaseModel):
    city: CityModel
    square_meter_rent: float

    class Config:
        orm_mode = True
