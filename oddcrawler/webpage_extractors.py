"""There are four main news source implemented for now: Monumental, La Prensa
 Libre, La Extra y CR Hoy."""

from abc import ABC, abstractmethod

class web_page():
    def __init__(self):
        self._main_url = None

    @abstractmethod
    def get_news_urls():
        pass

    @abstractmethod
    def filter_news_by_keywords():
        """From a list of urls, search within those urls certain keywords,
        and returns the ones that have a match."""
        pass

    @abstractmethod
    def extract_text_from_news():
        """Extract main news text from the url. The location of this text
        will be dependent of each newspaper."""
        pass

class monumental(web_page):
    def __init__(self, url):
        self._main_url = "http://www.monumental.co.cr/{_year}/{_month}/{_year}"

    def get_news_urls(datetime_date):
        self._year = datetime.date.year
        self._month = datetime.date.month
        self._day = datetime.date.day
        entry_point = self._main_url.format(**locals())

    def filter_news_by_keywords():
        pass

    def extract_text_from_news():
        pass
