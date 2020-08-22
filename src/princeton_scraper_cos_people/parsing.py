
import base64
import enum
import typing
import urllib.parse

import bs4
import requests

import princeton_scraper_cos_people.helpers


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "CosPersonType",
    "CosPersonInformation",
    "parse_cs_person",
]


class CosPersonType(enum.Enum):
    faculty = "faculty?type=main"
    affiliated_faculty = "faculty?type=associated"
    emeritus_faculty = "faculty?type=emeritus"
    researchers = "research"
    research_instructors = "researchinstructors"
    technical_staff = "restech"
    admin_staff = "admins"
    grad_students = "grad"

    def __str__(self):
        return self.name

    @classmethod
    def from_string(cls, name: str) -> typing.Optional[typing.Any]:
        for typname, typ in cls.__members__.items():
            if typname == name:
                return typ

            if typname == name.replace("-", "_"):
                return typ


# COS directory info type

CosPersonInformation = typing.TypedDict(
    "CosPersonInformation", {
        "netid": str,
        "email": str,
        "name": str,
        "first": str,
        "last": str,
        "profile-url": str,
        "image-url": str,
        "image": str,
        "website": str,
        "office": str,
        "phone": str,
        "research-areas": str,
        "research-interests": str,
        "title": str,
        "degree": str,
        "advisers": str,
        "type": str,
        "affiliations": str,
    }, total=False)


# Hard-coded constants that are required to scrape the web page

CS_URL_BASE = "https://www.cs.princeton.edu/"

CS_EMAIL_SPLITTER_FULL = "\xa0\xa0(&commatcs.princeton.edu)"
CS_EMAIL_SPLITTER_PARTIAL = "\xa0"
CS_EMAIL_SUFFIX_CLEAN = "@cs.princeton.edu"

CS_DEFAULT_IMG = "https://www.cs.princeton.edu/sites/all/modules/custom/cs_people/default.png"
CS_DEFAULT_IMG_FILENAME = "default.png"

CS_PROPERTY_ON_LEAVE = "(on leave)"


def _parse_cs_person_type(person_type):
    if type(person_type) is str:
        return CosPersonType.from_string(person_type)

    if type(person_type) is CosPersonType:
        return person_type


def parse_cs_person_types(person_type_or_types):
    if person_type_or_types is None:
        return []

    if type(person_type_or_types) is str and ("," in person_type_or_types or ";" in person_type_or_types):
        person_type_or_types = person_type_or_types.replace(",", ";")
        lst = list(map(str.strip, person_type_or_types.split(";")))
        return parse_cs_person_types(lst)

    if type(person_type_or_types) is not list:
        return parse_cs_person_types([person_type_or_types])

    if type(person_type_or_types) is list:
        return list(map(_parse_cs_person_type, person_type_or_types))

    return []


def clean_cs_email(
        str_or_dict: typing.Union[str, dict]
) -> typing.Optional[typing.Union[str, dict]]:
    if type(str_or_dict) is str:
        prefix = None

        if CS_EMAIL_SPLITTER_FULL in str_or_dict:
            prefix = str_or_dict.split(CS_EMAIL_SPLITTER_FULL)[0].strip()

        elif CS_EMAIL_SPLITTER_PARTIAL in str_or_dict:
            prefix = str_or_dict.split(CS_EMAIL_SPLITTER_PARTIAL)[0].strip()

        if prefix is not None:
            email = "{}{}".format(prefix, CS_EMAIL_SUFFIX_CLEAN)
            return email

    elif type(str_or_dict) is dict:
        email = clean_cs_email(str_or_dict.get("email", ""))
        if email is not None and email != "":
            str_or_dict["email"] = email
        return str_or_dict


def download_image(person: CosPersonInformation) -> CosPersonInformation:
    if "image-url" not in person:
        return person

    image_url = person["image-url"]
    response = requests.get(image_url)

    if not response.ok:
        return person

    # base64 encode the downloaded image and save in record
    image_b64 = base64.b64encode(response.content).decode()
    person["image"] = image_b64

    return person


def parse_cs_person(
        tag: bs4.Tag,
        person_type: typing.Optional[CosPersonType] = None,
) -> CosPersonInformation:
    record = {}

    def add_field(field, value):
        if value is not None:
            record[field] = value

    def add_field_from_tag(field, **kwargs):
        value = princeton_scraper_cos_people.helpers.extract_text(tag, default=None, **kwargs)
        add_field(field, value)

    add_field_from_tag("email", css_class="person-address-item", css_subclass="glyphicon-envelope")
    add_field_from_tag("office", css_class="person-address-item", css_subclass="glyphicon-briefcase")
    add_field_from_tag("degree", css_class="person-degree")
    add_field_from_tag("title", css_class="person-title")
    add_field_from_tag("name", css_class="person-name")
    add_field_from_tag("advisers", css_class="person-advisers")
    add_field_from_tag("research-areas", css_class="person-research-areas")
    add_field_from_tag("research-interests", css_class="person-research-interests")
    add_field_from_tag("affiliations", css_class="person-dept")

    # links
    add_field_from_tag("homepage", css_class="btn", css_subclass="glyphicon-globe",
                       postprocess=lambda tag: tag.get("href"))
    add_field_from_tag("profile-url", css_class="btn", css_subclass="glyphicon-arrow-right",
                       postprocess=lambda tag: tag.get("href"))

    # img
    imgtag = tag.find("img")
    if imgtag is not None and imgtag["src"] is not None:
        img_src = imgtag["src"]
        if CS_DEFAULT_IMG_FILENAME not in img_src:
            record["image-url"] = urllib.parse.urljoin(CS_URL_BASE, img_src)

    # postprocessing

    record = clean_cs_email(record)

    # NOTE: check that this is an NetID? not an alias?
    if "email" in record and "@cs.princeton.edu" in record["email"]:
        record["netid"] = record["email"].split("@")[0]

    if "profile-url" in record:
        record["profile-url"] = urllib.parse.urljoin(CS_URL_BASE,
                                                     record["profile-url"])

    if "name" in record:
        if CS_PROPERTY_ON_LEAVE in record["name"]:
            record["name"] = record["name"].replace(CS_PROPERTY_ON_LEAVE, "").strip()
            record["leave"] = True

    if "name" in record:
        first, last = princeton_scraper_cos_people.helpers.split_name(record["name"])
        record["first"] = first
        record["last"] = last

    if person_type is not None:
        record["type"] = str(person_type)

    return record



