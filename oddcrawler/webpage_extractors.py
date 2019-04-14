"""There are four main news source implemented for now: Monumental, La Prensa
 Libre, La Extra y CR Hoy."""

from abc import ABC, abstractmethod
from logging import getLogger
from datetime import timedelta, date
from json import dumps
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

    LOAD_TIMEOUT = 10
    MAX_DAYS_BEFORE = 7
    PAGE_NOT_FOUND = 'Page not found - Monumental'

    def __init__(self):
        self._main_url = "http://www.monumental.co.cr/{year}/{month}/{day}"
        self._subpage_url = "{main_url}/page/{page_number}"
        # If logger isn't configured outside this module, there won't be logs
        self._logger = getLogger(
            'oddcrawler.webpage_extractors.monumental_extractor')
        self._urls_xpath = '/html/body/div[3]/div[4]/section/div/div/section'
        self._articles_class = \
            'col-md-12 no-pad noticia noticia-vertical nota-interna listado'
        self._driver = Firefox()
        self._datetime_date = date.today()

    def __wait_until_page_loads(self):
        """Wait unitl LOAD_TIMEOUT seconds has passed, to confirm there's
        the xpath of the section that contains the news. If it isn't present,
        raise a TimeuutException."""
        WebDriverWait(self._driver, self.LOAD_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, self._urls_xpath)))

        self._logger.info('Page loaded succesfully')

    def __get_day_month_year_from_datetime(self, datetime_date):
        self._datetime_date = datetime_date
        self._year = datetime_date.year
        self._month = datetime_date.month
        self._day = datetime_date.day

    def __fetch_urls(self):
        """Format the main url with day, month and year, and command a driver
        to hit the formed url."""
        self._logger.info('Fetch urls from date {day}/{month}/{year}'.format(
            day=self._day,
            month=self._month,
            year=self._year))

        self._entry_url = self._main_url.format(day=self._day,
                                                month=self._month,
                                                year=self._year)

        self._logger.info('Entry point: {entry_url}'.format(
            entry_url=self._entry_url))

        self._logger.info('Starting a new driver using Firefox')
        self._driver.get(self._entry_url)

    def get_news_urls(self, datetime_date):
        """Try to get the urls from news of the start date. If page fails
        to load, then try with the previous day. Until a maximun of 7 days
        before the given datetime_date."""

        self.__get_day_month_year_from_datetime(datetime_date)

        loaded = False
        counter = self.MAX_DAYS_BEFORE
        self.news_urls = []

        # Get the date of the news right. Try to use the given one.
        # If it doesn't work, use the previous one
        while not loaded and counter > 0:
            counter -= 1
            try:
                self.__fetch_urls()

                self._logger.info('Wait until articles are formed, by xpath')
                self.__wait_until_page_loads()

                loaded = True
            except TimeoutException:
                # Try no longer than one week ago
                self.__get_day_month_year_from_datetime(
                    self._datetime_date - timedelta(days=1))

                # Assert the reason is the page doesn't exist
                assert self._driver.title == self.PAGE_NOT_FOUND

                self._logger.info(
                    'Page not found. Checking one day before.')

        # Now iterate through all pages, and return a list with all urls
        page = 1

        while self._driver.title != self.PAGE_NOT_FOUND:
            self._logger.info('Hitting page {number}'.format(number=page))

            self._logger.info('Get articles by tag name')
            articles = self._driver.find_elements_by_tag_name('article')

            for each_article in articles:
                assert each_article.get_attribute(
                    'class') == self._articles_class

                self.news_urls.append(
                    each_article.find_element_by_tag_name(
                        'a').get_attribute('href'))

            page += 1

            self._driver.get(self._subpage_url.format(
                main_url=self._entry_url,
                page_number=page))

        return self.news_urls

    def filter_news_by_keywords():
        pass

    def extract_text_from_news(self):
        """Given that the news urls has been resolved, extract the text from
        all news urls. Create a dictionary, which contains the url of the
        news as keys, and the text as values."""

        result = {}

        for each_new_url in self.news_urls:
            self._logger.info(
                'Extract data from {url}'.format(url=each_new_url))

            self._driver.get(each_new_url)

            all_paragraphs = self._driver.find_elements_by_tag_name('p')

            for p in all_paragraphs:
                print(p.get_attribute('style'))
                if p.get_attribute('style') == 'text-align: justify;':
                    print('match')
                    print(p.text)
                else:
                    print('nomatch')

            valid_paragraphs = [p.text if p.get_attribute('style') ==
                                'text-align: justify;' else '' for p in
                                self._driver.find_elements_by_tag_name('p')]

            result[each_new_url] = ' '.join(valid_paragraphs)

        # Just in case we are running with set on force urls
        # Define day, month and year, with the date defined at build time
        # in __init__.
        self.__get_day_month_year_from_datetime(self._datetime_date)

        # Write result to a file, with current date.
        with open('complete_news_from_{day}_{month}_{year}'.format(
                day=self._day,
                month=self._month,
                year=self._year), 'w') as f:
            f.write(dumps(result))
            f.close()

        return result

    def __del__(self):
        self._driver.quit()
