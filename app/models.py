from sqlalchemy import Column, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from app.core.config import get_settings

engine = create_engine(get_settings().DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True)
    code = Column(String(3), unique=True, nullable=False)
    name = Column(String(100), nullable=True)


class City(Base):
    __tablename__ = "city_information"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    insee_code = Column(String(10), unique=True, nullable=False)

    rating = Column(Float, nullable=True)
    population = Column(Integer, nullable=False)

    department_id = Column(
        Integer, ForeignKey(Department.id), nullable=False, index=True
    )
    department = relationship(
        Department, backref="cities", foreign_keys=[department_id]
    )


class ApartmentRentIndicator(Base):
    """
    Appartment Rent Indicators Model
    - We decided for this model to only store the fields below
      (the only ones that we will need here)
    """

    __tablename__ = "apartment_rent_indicator"

    id = Column(Integer, primary_key=True)

    square_meter_rent = Column(Float, nullable=False)

    city_id = Column(Integer, ForeignKey(City.id), nullable=False, index=True)
    city = relationship(City, backref="indicators", foreign_keys=[city_id])

    department_id = Column(
        Integer, ForeignKey(Department.id), nullable=False, index=True
    )
    department = relationship(
        Department, backref="indicators", foreign_keys=[department_id]
    )


class CityZipCode(Base):
    __tablename__ = "city_zipcode"
    id = Column(Integer, primary_key=True)
    zipcode = Column(
        String(15), nullable=False
    )  # We leave some place for special characters and long zipcodes
    city_id = Column(Integer, ForeignKey(City.id), nullable=False, index=True)
    city = relationship(City, backref="zipcodes", foreign_keys=[city_id])
