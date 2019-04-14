
from datetime import timedelta, date
from logging import getLogger
from json import dumps, loads
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException

from oddcrawler.webpage_extractors import WebpageExtractor

class MonumentalExtractor(WebpageExtractor):

    LOAD_TIMEOUT = 10
    MAX_DAYS_BEFORE = 7
    PAGE_NOT_FOUND = 'Page not found - Monumental'

    def __init__(self):
        self._main_url = 'http://www.monumental.co.cr/{year}/{month}/{day}'
        self._subpage_url = "{main_url}/page/{page_number}"
        # If logger isn't configured outside this module, there won't be logs
        self._logger = getLogger(
            'oddcrawler.webpage_extractors.MonumentalExtractor')
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

    def __fetch_urls(self):
        """Format the main url with day, month and year, and command a driver
        to hit the formed url."""
        self._logger.info('Fetch urls from date {day2}/{month}/{year}'.format(
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

        super(
            MonumentalExtractor,
            self
        )._get_day_month_year_from_datetime(datetime_date)

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
                super(
                    MonumentalExtractor,
                    self
                )._get_day_month_year_from_datetime(
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

            self._complete_news_info[each_new_url] = ' '.join(valid_paragraphs)

        # Just in case we are running with set on force urls
        # Define day, month and year, with the date defined at build time
        # in __init__.
        super(
            MonumentalExtractor,
            self
        )._get_day_month_year_from_datetime(self._datetime_date)

        # Write self._complete_news_info to a file, with current date.
        with open('complete_news_of_monumental_from_{day}_{month}_{year}.json'
                  ''.format(day=self._day,
                            month=self._month,
                            year=self._year), 'w') as f:
            f.write(dumps(self._complete_news_info))
            f.close()

        return self._complete_news_info

    def filter_news_by_keywords(self, keywords: list) -> dict:
        """Given the complete information from news, return a dictionary
        that only contains news in which the text contains one of the
        keywords asked for."""

        self._logger.info(
            'Appling filters to info using this keywords: {keywords}'.format(
                **locals()))

        # BEGINS HACK
        # Don't wait until extract_text is done.

        with open('complete_news_from_13_4_2019', 'r') as f:
            self._complete_news_info = loads(f.read())
            f.close()

        # ENDS HACK

        self._filtered_news_info = {'keywords': keywords}

        for key, value in self._complete_news_info.items():
            match = False
            for each_keyword in keywords:
                # Only one match is enough
                if each_keyword.lower() in value.lower():
                    match = True
                    break

            if match:
                self._logger.info('Hit found with {url}'.format(url=key))
                self._filtered_news_info[key] = value

        # Just in case we are running with set on force urls
        # Define day, month and year, with the date defined at build time
        # in __init__.
        super(
            MonumentalExtractor,
            self
        )._get_day_month_year_from_datetime(self._datetime_date)

        # Write the filtered result in disk
        with open('filtered_news_of_monumental_from_{day}_{month}_{year}.json'
                  ''.format(
                      day=self._day,
                      month=self._month,
                      year=self._year), 'w') as f:
            f.write(dumps(self._filtered_news_info))
            f.close()

        return self._filtered_news_info

    def __del__(self):
        self._driver.quit()
