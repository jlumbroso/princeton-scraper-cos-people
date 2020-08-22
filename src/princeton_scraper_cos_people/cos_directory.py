
import typing
import urllib.parse

import requests
import bs4

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


def _fetch_cos_people_directory(
        person_type: princeton_scraper_cos_people.parsing.CosPersonType
) -> typing.List[princeton_scraper_cos_people.parsing.CosPersonInformation]:
    url = _build_directory_url(person_type)
    response = requests.get(url)

    if not response.ok:
        return []

    soup = bs4.BeautifulSoup(response.content, features="html.parser")

    div_list = soup.find_all("div", {"class": "person"})
    person_list = list(filter(lambda obj: obj is not None, map(
        lambda tag: princeton_scraper_cos_people.parsing.parse_cs_person(
            tag=tag,
            person_type=person_type),
        div_list
    )))

    return person_list


# noinspection PyBroadException
def fetch_cos_people_directory(
        person_types: typing.Optional[typing.List[princeton_scraper_cos_people.parsing.CosPersonType]] = None,
        download_images: bool = False,
) -> typing.List[princeton_scraper_cos_people.parsing.CosPersonInformation]:

    records = []

    if person_types is None:
        person_types = princeton_scraper_cos_people.parsing.CosPersonType.__members__.values()

    for person_type in person_types:

        person_list = _fetch_cos_people_directory(
            person_type=person_type,
        )

        if person_list is not None and len(person_list) > 0:
            records += person_list

    # let's not fail because the images couldn't be downloaded
    if download_images:
        try:
            records = list(map(princeton_scraper_cos_people.parsing.download_image, records))
        except:
            pass

    return records
