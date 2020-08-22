
import datetime
import json
import typing

import comma

import princeton_scraper_cos_people.cos_directory
import princeton_scraper_cos_people.parsing


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "json_output",
    "csv_output",
]


# noinspection PyBroadException
def json_output(
        person_types: typing.Optional[typing.List[princeton_scraper_cos_people.parsing.CosPersonType]],
        download_images=False,
) -> typing.Optional[str]:
    try:
        data = princeton_scraper_cos_people.cos_directory.fetch_cos_people_directory(
            person_types=person_types,
            download_images=download_images,
        )

        return json.dumps({
            "source": "https://github.com/jlumbroso/princeton-scraper-cos-people/",
            "timestamp": datetime.datetime.now().isoformat(),
            "data": data,
        }, indent=2)
    except Exception:
        raise
        return


def csv_output(
        person_types: typing.Optional[typing.List[princeton_scraper_cos_people.parsing.CosPersonType]],
) -> typing.Optional[str]:
    try:
        data = princeton_scraper_cos_people.cos_directory.fetch_cos_people_directory(
            person_types=person_types,
            download_images=False,
        )
        # for row in data:
        #     del row["research"]
        #     row["affiliations"] = ";".join(row["affiliations"])
        return comma.dumps(data)
    except Exception:
        return
