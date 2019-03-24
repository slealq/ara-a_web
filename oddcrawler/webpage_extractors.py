"""There are four main news source implemented for now: Monumental, La Prensa
 Libre, La Extra y CR Hoy."""

from abc import ABC, abstractmethod
from logging import getLogger
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException

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
        # If logger isn't configured outside this module, there won't be logs
        self._logger = getLogger(
            'oddcrawler.webpage_extractors.monumental_extractor')
        self._urls_xpath = '/html/body/div[3]/div[4]/section/div/div/section'
        self._urls_class = 'col-md-7 col-xs-12 content-noticias archive'
        self._driver = Firefox()

    def wait_until_page_loads(self):
        TIMEOUT = 10
        try:
            WebDriverWait(self._driver, TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, self._urls_xpath)))
        except TimeoutException:
            raise WebDriverException("Page didn't load correctly")

    def get_news_urls(self, datetime_date):
        year = datetime_date.year
        month = datetime_date.month
        day = datetime_date.day

        self._logger.info(
            'Fetch urls from date {day}/{month}/{year}'.format(**locals()))
        entry_url = self._main_url.format(**locals())

        self._logger.info('Entry point: {entry_url}'.format(
            entry_url=entry_url))

        self._logger.info('Starting a new driver using Firefox')
        self._driver.get(entry_url)

        self._logger.info('Wait until articles are formed, by xpath')
        self.wait_until_page_loads()

        self._logger.info('Get urls using class')
        urls = self._driver.find_elements_by_class_name(self._urls_class)

        return [urls]

    def filter_news_by_keywords():
        pass

    def extract_text_from_news():
        pass

    def __del__(self):
        self._driver.quit()
