
import requests
import bs4


#from princeton_scraper_seas_faculty import __version__


SOME_LOW_TENS_NUMBER = 14


# def test_version():
#     assert __version__ == '0.1.0'


def test_faculty_format_dom():
    r = requests.get("https://www.cs.princeton.edu/people/faculty")
    assert r.ok

    s = bs4.BeautifulSoup(r.content, features="html.parser")
    assert s is not None

    people = s.find_all("div", {"class": "people"})
    person = s.find_all("div", {"class": "person"})

    assert len(people) == 1
    assert len(person) > SOME_LOW_TENS_NUMBER


