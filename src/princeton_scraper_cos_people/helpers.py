
import typing

import bs4


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "split_name",
    "extract_text",
]


CS_SCRAPING_LABEL_CLASS = "person-label"


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


# noinspection PyBroadException
def extract_text(
        tag: bs4.Tag,
        css_class: typing.Optional[str] = None,
        css_subclass: typing.Optional[str] = None,
        default: typing.Optional[str] = None,
        postprocess: typing.Optional[typing.Callable[[bs4.Tag], str]] = None,
        remove_label_text: bool = True,
):
    if tag is None:
        return default

    if css_subclass is not None:
        tags = tag.find_all(attrs={"class": css_class})
        tags = list(filter(lambda t: t.find(attrs={"class": css_subclass}) is not None, tags))

        if len(tags) == 0:
            return

        tag = tags[0]

    elif css_class is not None:
        tag = tag.find(attrs={"class": css_class})

    try:
        labeltag = tag.find(attrs={"class": CS_SCRAPING_LABEL_CLASS})
        labeltext = "" if labeltag is None else labeltag.text

        if postprocess is not None:
            try:
                return postprocess(tag)
            except:
                pass

        text = tag.text.strip()
        if remove_label_text and labeltext != "":
            text = text.replace(labeltext, "").strip()

        return text
    except:
        return default


