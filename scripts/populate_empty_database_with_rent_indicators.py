import argparse
import csv
import os.path

from app.core.session import get_session
from app.models import ApartmentRentIndicator, City, CityZipCode, Department
from app.utils.city_informations import CityInfosService
from app.utils.gov_geo import GouvAPIGeoService

"""
A script that helps to populate database starting from zero
Note: this is a very dumb script that does the job
 - lack a lot of error handling (sorry)
"""

# flake8: noqa: C901
if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--filepath", required=True, help="The path to the filename to import", type=str
    )
    arg_parser.add_argument(
        "--encoding",
        required=False,
        default="utf-8",
        help="The path to the filename to import",
        type=str,
    )
    args = arg_parser.parse_args()
    filepath = args.filepath
    encoding = args.encoding
    if not os.path.exists(filepath):
        print(f"Error: {filepath}: no such file or directory")
        exit(0)

    departments_ids = (
        {}
    )  # Will be used as a dict to store department ids (key = department id)
    cities_ids = {}  # Will be used as a dict to store city ids (key = insee code)

    csv_file = open(filepath, mode="r", encoding=encoding)
    csv_reader = csv.DictReader(csv_file, delimiter=";")
    failed_lines = []
    session = next(get_session())

    for row in csv_reader:
        # Validate input
        # If there's an error raise it
        row_data = None
        department_key = row["DEP"].zfill(2)
        city_key = row["INSEE"].zfill(5)
        department_id = departments_ids.get(department_key, None)
        city_id = cities_ids.get(city_key, None)

        if not department_id:
            infos = GouvAPIGeoService.retrieve_department_informations(
                department_code=department_key
            )

            if not infos:
                failed_lines.append(row)
                continue
            department = Department(code=infos["code"], name=infos["nom"])
            session.add(department)
            session.commit()
            session.refresh(department)
            department_id = department.id
            departments_ids[department_key] = department.id

        if not city_id:
            city_infos = GouvAPIGeoService.retrieve_city_informatins(inseeCode=city_key)

            if not city_infos:
                failed_lines.append(row)
                continue

            rating = CityInfosService.retrieve_city_rating(cityName=city_infos["nom"])

            # scrapping being a little bit too long (a random value would do the job)
            # rating = round(random.random() * 5, 2)

            city = City(
                insee_code=city_key,
                name=city_infos["nom"],
                rating=rating,
                population=city_infos["population"],
                department_id=department_id,
            )
            session.add(city)
            session.commit()
            session.refresh(city)
            city_id = city.id

            zipcodes = (
                CityZipCode(zipcode=zip, city_id=city_id)
                for zip in city_infos["codesPostaux"]
            )
            session.add_all(zipcodes)
            session.commit()
        session.add(
            ApartmentRentIndicator(
                department_id=department_id,
                city_id=city_id,
                square_meter_rent=float(row["loypredm2"].replace(",", ".")),
            )
        )
        session.commit()
    if failed_lines:
        print("import failed for the following lines:")
        for line in failed_lines:
            print(line)
