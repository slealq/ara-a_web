from datetime import timedelta
from logging import getLogger
from json import dumps
from selenium.common.exceptions import TimeoutException

from oddcrawler.webpage_extractors import WebpageExtractor


class MonumentalExtractor(WebpageExtractor):
    NAME = 'monumental'
    LOAD_TIMEOUT = 10
    MAX_DAYS_BEFORE = 7
    PAGE_NOT_FOUND = 'Page not found - Monumental'

    def __init__(self):
        self._logger = getLogger(
            'oddcrawler.webpage_extractors.MonumentalExtractor')
        super(MonumentalExtractor, self).__init__(
        )
        self._main_url = 'http://www.monumental.co.cr/{year}/{month}/{day}'
        self._subpage_url = "{main_url}/page/{page_number}"
        # If logger isn't configured outside this module, there won't be logs

        self._urls_xpath = '/html/body/div[3]/div[4]/section/div/div/section'
        self._articles_class = \
            'col-md-12 no-pad noticia noticia-vertical nota-interna listado'
        self._logger.info('Starting a new driver using Firefox')

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

        self._driver.get(self._entry_url)

    def get_news_urls(self, datetime_date):
        """Try to get the urls from news of the start date. If page fails
        to load, then try with the previous day. Until a maximun of 7 days
        before the given datetime_date."""

        self._get_day_month_year_from_datetime(datetime_date)

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
                self._wait_until_page_loads(self._urls_xpath)

                loaded = True
            except TimeoutException:
                # Try no longer than one week ago
                self._get_day_month_year_from_datetime(
                    self._datetime_date - timedelta(days=1))

                # Assert the reason is the page doesn't exist
                assert self._driver.title == self.PAGE_NOT_FOUND

                self._logger.info(
                    'Page not found. Checking one day before.')

        # Now iterate through all pages, and return a list with all urls
        page = 1

        self._logger.info('Page loaded succesfully')

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

    def extract_text_from_news(self):
        """Given that the news urls has been resolved, extract the text from
        all news urls. Create a dictionary, which contains the url of the
        news as keys, and the text as values."""

        self._complete_news_info = {}

        for each_new_url in self.news_urls:
            self._logger.info(
                'Extract data from {url}'.format(url=each_new_url))

            self._driver.get(each_new_url)

            all_paragraphs = self._driver.find_elements_by_tag_name('p')

            valid_paragraphs = [p.text if p.get_attribute('style') ==
                                'text-align: justify;' else '' for p in
                                self._driver.find_elements_by_tag_name('p')]

            self._complete_news_info[each_new_url] = ' '.join(valid_paragraphs)

        # Just in case we are running with set on force urls
        # Define day, month and year, with the date defined at build time
        # in __init__.
        self._get_day_month_year_from_datetime(self._datetime_date)

        # Write self._complete_news_info to a file, with current date.
        with open('complete_news_of_{name}_from_{day}_{month}_{year}.json'
                  ''.format(name=self.NAME,
                            day=self._day,
                            month=self._month,
                            year=self._year), 'w') as f:
            f.write(dumps(self._complete_news_info))
            f.close()

        return self._complete_news_info

    def __del__(self):
        self._logger.info('Closing browser.')
        self._driver.quit()
