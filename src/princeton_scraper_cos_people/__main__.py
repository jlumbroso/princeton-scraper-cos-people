
import sys

import princeton_scraper_cos_people.output
import princeton_scraper_cos_people.parsing


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"


# noinspection PyBroadException
if __name__ == "__main__":

    is_csv = False
    has_images = False
    person_types = None

    # "parse" command line parameter
    # NOTE: should be a real command line tool

    if len(sys.argv) > 0:
        if "--csv" in sys.argv:
            is_csv = True

        if "--img" in sys.argv:
            has_images = True

        lst = sys.argv[:]
        lst_types = list(filter(
            lambda obj: obj is None,
            map(princeton_scraper_cos_people.parsing.parse_cs_person_types,
                lst)
        ))

        if len(lst_types) > 0:
            person_types = lst_types

    # output selected format

    output = None
    if is_csv:
        output = princeton_scraper_cos_people.output.csv_output(person_types=person_types)
    else:
        output = princeton_scraper_cos_people.output.json_output(
            person_types=person_types,
            download_images=has_images,
        )

    if output is None:
        sys.exit(1)
    else:
        print(output)
        sys.exit(0)
