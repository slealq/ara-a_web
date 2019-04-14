"""There are four main news source implemented for now: Monumental, La Prensa
 Libre, La Extra y CR Hoy."""

from abc import ABC, abstractmethod
from logging import getLogger

# create logger
_logger = getLogger('oddcrawler.webpage_extractors')


class WebpageExtractor(ABC):
    def __init__(self):
        self._main_url = None

    def _get_day_month_year_from_datetime(self, datetime_date):
        self._datetime_date = datetime_date
        self._year = datetime_date.year
        self._month = datetime_date.month
        self._day = datetime_date.day

    @abstractmethod
    def get_news_urls():
        pass

    @abstractmethod
    def extract_text_from_news():
        """Extract main news text from the url. The location of this text
        will be dependent of each newspaper."""
        pass

    @abstractmethod
    def filter_news_by_keywords():
        pass
