
import datetime
import os
import json
import sys

import princeton_scraper_cos_people.output
import princeton_scraper_cos_people.parsing


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"


# noinspection PyBroadException
if __name__ == "__main__":

    is_csv = False
    has_images = False
    person_types = None
    generate_feeds = False
    feeds_output = None

    # "parse" command line parameter
    # NOTE: should be a real command line tool

    if len(sys.argv) > 0:
        argv = sys.argv[:]

        if "--csv" in argv:
            is_csv = True
            argv.remove("--csv")

        if "--img" in sys.argv:
            has_images = True
            argv.remove("--img")

        # NOTE: should use a command line parser!
        if "--feeds" in sys.argv:
            generate_feeds = True
            feed_output_index = argv.index("--feeds") + 1
            if feed_output_index != 0 and feed_output_index < len(argv):
                feeds_output = argv[feed_output_index]

            del argv[feed_output_index]
            argv.remove("--feeds")

        lst = sys.argv[:]
        lst_types = list(filter(
            lambda obj: obj is None,
            map(princeton_scraper_cos_people.parsing.parse_cs_person_types,
                lst)
        ))

        if len(lst_types) > 0:
            person_types = lst_types

    # generate feeds
    if generate_feeds:
        save_all = False
        if person_types is None:
            person_types = princeton_scraper_cos_people.parsing.CosPersonType.__members__.values()
            save_all = True

        records = []
        for person_type in person_types:
            output = princeton_scraper_cos_people.output.json_output(
                person_types=[person_type],
                download_images=has_images,
            )
            records += json.loads(output).get("data", [])

            dirpath = os.path.join(feeds_output, "feeds", "{}/".format(str(person_type)))
            filepath = os.path.join(dirpath, "index.json")

            # ensure the folder exists
            try:
                os.makedirs(dirpath)
            except FileExistsError:
                pass

            with open(filepath, "w") as f:
                f.write(output)

        filepath = os.path.join(feeds_output, "feeds", "index.json")
        with open(filepath, "w") as f:
            f.write(json.dumps({
                "source": "https://github.com/jlumbroso/princeton-scraper-cos-people/",
                "timestamp": datetime.datetime.now().isoformat(),
                "data": records,
            }, indent=2))

        sys.exit(0)

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
