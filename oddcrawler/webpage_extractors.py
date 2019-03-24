"""There are four main news source implemented for now: Monumental, La Prensa
 Libre, La Extra y CR Hoy."""

from abc import ABC, abstractmethod
from logging import getLogger

# create logger
module_logger = getLogger('oddcrawler.webpage_extractors')

class webpage_extractor(ABC):
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


class monumental_extractor(webpage_extractor):
    def __init__(self):
        self._main_url = "http://www.monumental.co.cr/{year}/{month}/{day}"
        # If no logger is configured outside this module, there will be no
        # info
        self._logger = getLogger(
            'oddcrawler.webpage_extractors.monumental_extractor')

    def get_news_urls(self, datetime_date):
        year = datetime_date.year
        month = datetime_date.month
        day = datetime_date.day
        self._logger.info(
            'Fetch urls from date {day}/{month}/{year}'.format(**locals()))
        entry_url = self._main_url.format(**locals())
        self._logger.info('Entry point: {entry_url}'.format(
            entry_url=entry_url))

        return []

    def filter_news_by_keywords():
        pass

    def extract_text_from_news():
        pass
