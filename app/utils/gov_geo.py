import logging

import requests

_logger = logging.getLogger(__name__)


class GouvAPIGeoService:
    _CITY_GEO_API_URL = "https://geo.api.gouv.fr/communes/"
    _DEPARTMENT_GEO_API_URL = "https://geo.api.gouv.fr/departements/"

    @classmethod
    def retrieve_city_informatins(cls, inseeCode: str) -> dict:
        """
        Retrieves city data from gov geodata
        :param inseeCode: city's INSEE code
        :return:
        """

        # As gov api should be requested with strings that represent
        # insee codes that are
        # At least 5 characters long we
        insee_code_str = inseeCode.zfill(5)

        response = requests.request(
            method="GET", url=f"{cls._CITY_GEO_API_URL}{insee_code_str}"
        )
        if response.status_code != 200:
            logging.error(
                f"failed at retrieving city informations for {insee_code_str}"
            )
            return {}

        return response.json()

    @classmethod
    def retrieve_department_informations(cls, department_code: str) -> dict:
        """
        Retrieves department data from gov geodata
        :param department_code:
        :return:
        """
        complete_department_code = department_code.zfill(2)
        response = requests.request(
            method="GET", url=f"{cls._DEPARTMENT_GEO_API_URL}{complete_department_code}"
        )

        if response.status_code != 200:
            logging.error(
                f"failed at retrieving city informations for {department_code}"
            )
            return {}

        return response.json()
