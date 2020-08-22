
import enum
import typing
import urllib.parse

import requests
import bs4

import princeton_scraper_cos_people.campus_directory
import princeton_scraper_cos_people.constants
import princeton_scraper_cos_people.helpers
import princeton_scraper_cos_people.parsing


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "fetch_cos_people_directory",
]


#  URL to retrieve the COS directory

PRINCETON_CS_URL_BASE = "https://www.cs.princeton.edu/"
PRINCETON_CS_DIRECTORY_BASE = "https://www.cs.princeton.edu/people/"


def _build_directory_url(
        person_type: princeton_scraper_cos_people.parsing.CosPersonType
) -> str:
    value = person_type.value
    url = urllib.parse.urljoin(PRINCETON_CS_DIRECTORY_BASE, value)
    return url


def fetch_cos_people_directory() -> typing.List[princeton_scraper_cos_people.parsing.CosPersonInformation]:

    records = []

    for typname, typ in princeton_scraper_cos_people.parsing.CosPersonType.__members__.items():
        url = _build_directory_url(typ)
        response = requests.get(url)
        if response.ok:
            soup = bs4.BeautifulSoup(response.content, features="html.parser")
            div_list = soup.find_all("div", {"class": "person"})
            person_list = list(filter(lambda obj: obj is not None, map(
                lambda tag: princeton_scraper_cos_people.parsing.parse_cs_person(tag=tag, person_type=typ),
                div_list
            )))
            if len(person_list) > 0:
                records = records + person_list

    return records
