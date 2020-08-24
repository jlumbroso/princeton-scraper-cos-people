# Princeton COS People Scraper

This is a web scraper that produces machine-processable JSON feeds
of Princeton University's Department of Computer Science directory, sourced
from [the official, publicly available directory](https://www.cs.princeton.edu/people).

You can see [the main JSON feed by clicking here](https://jlumbroso.github.io/princeton-scraper-cos-people/feeds/).

There are also sub-feeds by category of persons (faculty, grad students, staff, etc.).
These feeds are all updated *every week on Saturday*. Read on to learn more.

## Accessing the static feeds

You can access the main (regularly updated) JSON feed directly from this URL:
```text
https://jlumbroso.github.io/princeton-scraper-cos-people/feeds/
```

There are sub-feeds available for the different categories of people:
- [`admin-staff`](https://jlumbroso.github.io/princeton-scraper-cos-people/feeds/admin-staff/)
- [`affiliated-faculty`](https://jlumbroso.github.io/princeton-scraper-cos-people/feeds/affiliated-faculty/)
- [`emeritus-faculty`](https://jlumbroso.github.io/princeton-scraper-cos-people/feeds/emeritus-facultyf/)
- [`faculty`](https://jlumbroso.github.io/princeton-scraper-cos-people/feeds/faculty/)
- [`grad-students`](https://jlumbroso.github.io/princeton-scraper-cos-people/feeds/grad-students/)
- [`research-instructors`](https://jlumbroso.github.io/princeton-scraper-cos-people/feeds/research-instructors/)
- [`researchers`](https://jlumbroso.github.io/princeton-scraper-cos-people/feeds/researchers/)
- [`technical-staff`](https://jlumbroso.github.io/princeton-scraper-cos-people/feeds/technical-staff/)

For example using Python, you can use the `requests` package to
get the JSON feed:
```python
import requests
r = requests.get("https://jlumbroso.github.io/princeton-scraper-cos-people/feeds/")
if r.ok:
    data = r.json()["data"]
```
## Feed format

This feed provides most people in the directory as a JSON dictionary with
the following fields:

```json
    {
        "email": "lumbroso@cs.princeton.edu",
        "office": "035 Corwin Hall",
        "degree": "Ph.D., Universit\u00e9 Pierre et Marie Curie, 2012",
        "title": "Lecturer",
        "name": "J\u00e9r\u00e9mie Lumbroso",
        "research-interests": "Probabilistic algorithms, data streaming, data structures, analysis of algorithms, analytic combinatorics.",
        "profile-url": "https://www.cs.princeton.edu/people/profile/lumbroso",
        "image-url": "https://www.cs.princeton.edu/sites/all/modules/custom/cs_people/generate_thumbnail.php?id=2488&thumb=",
        "image": "<base 64 encoded JPEG of the image>",
        "netid": "lumbroso",
        "first": "J\u00e9r\u00e9mie",
        "last": "Lumbroso",
        "type": "faculty"
    }
```

Other categories of people may have other fields, such as `leave`, `advisers`, `website`, etc.

## Backstory

Previously, I had implemented [JSON feeds to programmatically obtain the faculty of
Princeton's School of Engineering and Applied Sciences](https://github.com/jlumbroso/princeton-scraper-seas-faculty/),
to build the web portal for the BSE 2024 First Year Advising program.

This time, I needed to access the directory information of the Department of Computer Science
graduate students. Unfortunately, like for the SEAS faculty, there is no programmatically
available data source that also contains important information such as photos; the only such
source is the Department of Computer Science official website.

Despite having had conversations with [@sckarlin](https://github.com/sckarlin) about not
scraping the contents of the directory, it appeared that this was the easiest way to obtain
up-to-date grad student information.

The first application for this feed will be to configure and provision the Slack profiles of
the CS grad student Slack.

## License

This repository is licensed under [_The Unlicense_](LICENSE). This means I have no liability, but
you can do absolutely what you want with this.