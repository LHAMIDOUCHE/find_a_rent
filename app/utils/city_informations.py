import requests
from bs4 import BeautifulSoup


class CityInfosService:
    """
    CityInfos service

    A class with static methods that help

    """

    _BIEN_DANS_MA_VILLE_URL = "https://www.bien-dans-ma-ville.fr/"

    @classmethod
    def retrieve_city_rating(cls, cityName: str) -> float:
        """
        Retrieves the average review on the city by searching and scrapping
        on bien dans ma ville

        - Why searching and scrapping ?
           - Searching helps to retrieve the appropriate link for the targeted city
           - Once we have the link --> we scrap the page
                (a little of retro engineering)
        If the page design changes we could be in a kind of trouble.
        I assumed that the page wouldn't change during the exercice.
        I also didn't look further if there was an API
        :param cityName: the name of the city
        :return: the average rating of the city if found within the page
        of the city or None otherwise
        """
        if not cityName:
            return None
        response = requests.post(
            url=cls._BIEN_DANS_MA_VILLE_URL, data=dict(a="search", q=cityName)
        )
        if response.status_code != 200:
            return None

        city_link_content = response.content
        bs = BeautifulSoup(city_link_content, "lxml")
        links = bs.findAll("a")
        if not links:
            return None

        link = links[0].get("href") + "avis.html"

        response = requests.get(url=link)
        if response.status_code != 200:
            return None

        page_content = response.content
        bs = BeautifulSoup(page_content, "lxml")
        noteMoy = bs.findAll("div", {"class": "bloc_notemoyenne"})
        if not noteMoy:
            return None

        total = bs.find("div", {"class": "total"})
        if not total:
            return None

        return float(total.contents[0])
