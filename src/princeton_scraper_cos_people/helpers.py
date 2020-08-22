
import typing

import requests
import bs4


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "split_name",
    "extract_text",
]


def split_name(name: str) -> typing.Tuple[str, str]:
    """
    Returns a likely `(first, last)` split given a full name. This uses
    very simple heuristics, and assumes Western usage.

    :param name: A full name (first and last name).
    :return: A split pair with the first names, and the last name.
    """
    words = name.split()

    first_bits = words[:-1]
    last_bits = words[-1:]
    while len(first_bits) > 0 and first_bits[-1][0].islower():
        last_bits = [first_bits[-1]] + last_bits
        first_bits = first_bits[:-1]

    first_joined = " ".join(first_bits)
    last_joined = " ".join(last_bits)

    return first_joined, last_joined


def extract_text(tag, css_class=None, css_subclass=None, default=None):
    if tag is None:
        return default

    if css_subclass is not None:
        tags = tag.find_all(attrs={"class": css_class})
        tags = list(filter(lambda tag: tag.find(attrs={"class": css_subclass}) is not None, tags))
        tag = tags[0]

    elif css_class is not None:
        tag = tag.find(attrs={"class": css_class})

    try:
        return tag.text.strip()
    except:
        return default


