
"""
Library to fetch and parse the public Princeton SEAS Faculty directory as a
Python dictionary or JSON data source.
"""

__version__ = '1.0.0'

__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "CosPersonType",
    "CosPersonInformation",
    "fetch_cos_people_directory",
]


from princeton_scraper_cos_people.parsing import CosPersonType
from princeton_scraper_cos_people.parsing import CosPersonInformation
from princeton_scraper_cos_people.cos_directory import fetch_cos_people_directory


version_info = tuple(int(v) if v.isdigit() else v for v in __version__.split('.'))

