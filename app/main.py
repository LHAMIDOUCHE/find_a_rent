from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.session import get_session
from app.models import ApartmentRentIndicator, City, CityZipCode, Department
from app.schemas import IndicatorModel, RequestModel


def get_application():
    _app = FastAPI(title=get_settings().PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in get_settings().BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()


@app.post("/search")
async def search(
    request: RequestModel, db: Session = Depends(get_session)
) -> List[IndicatorModel]:
    requested_price = request.maximum_rent_price / request.surface

    department = db.query(Department).filter_by(code=request.department).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail=f"Could not find a corresponding department "
                   f"to code {request.department}",
        )

    selected_indicators = (
        db.query(ApartmentRentIndicator)
        .join(City)
        .join(CityZipCode)
        .filter(
            and_(
                ApartmentRentIndicator.department_id == department.id,
                ApartmentRentIndicator.square_meter_rent <= requested_price,
            )
        )
        .all()
    )

    return [
        IndicatorModel(
            city=indicator.city, square_meter_rent=indicator.square_meter_rent
        )
        for indicator in selected_indicators
    ]
