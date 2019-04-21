from logging import getLogger
from json import dumps
from selenium.common.exceptions import TimeoutException
from oddcrawler.webpage_extractors import WebpageExtractor


class LaPrensaLibreExtractor(WebpageExtractor):
    NAME = 'la_prensa_libre'
    URL_SECTION_TIMEOUT = 1
    PARAGRAPH_TIMEOUT = 1

    def __init__(self):
        # Logger needs to be defined before the super constructor is called
        self._logger = getLogger(
            'oddcrawler.webpage_extractors.LaPrensaLibreExtractor')
        super(LaPrensaLibreExtractor, self).__init__()

        # Now define this subclass variables properly
        self._main_url =\
            'http://www.laprensalibre.cr/Noticias/index/{year}-{month}-{day}/'
        self._urls_section_xpath = '/html/body/div[2]/div'
        self._urls_xpath = '/html/body/div[2]/div/a[{number}]'

    def get_news_urls(self, datetime_date):
        """Get the urls from the start date."""

        self._get_day_month_year_from_datetime(datetime_date)
        self.news_urls = []

        try:
            self._logger.info(
                'Fetch urls from date {day}/{month}/{year}'.format(
                    day=self._day,
                    month=self._month,
                    year=self._year))
            self._entry_url = self._main_url.format(year=self._year,
                                                    month=self._month,
                                                    day=self._day)
            self._logger.info('Entry point: {entry_url}'.format(
                entry_url=self._entry_url))
            self._driver.get(self._entry_url)
            self._logger.info('Wait until articles are formed, by xpath')
            self._wait_until_page_loads(self._urls_section_xpath)
        except TimeoutException:
            self._logger.info('Page not found. Time out')

        self._logger.info('Page loaded succesfully')

        # Try to grab next news, by xpath. If timeout exists, assume
        # it is because that's the end.
        exception_thrown = False
        news_index = 1
        while not exception_thrown:
            try:
                self._wait_until_page_loads(
                    self._urls_xpath.format(number=news_index),
                    self.URL_SECTION_TIMEOUT
                )

                link_a = self._driver.find_element_by_xpath(
                    self._urls_xpath.format(
                        number=news_index)).get_attribute('href')

                self.news_urls.append(link_a)

                news_index += 1

            except TimeoutException:
                self._logger.info(
                    'Got {news_number} news. Is that right?'.format(
                        news_number=news_index-1))

                exception_thrown = True

        return self.news_urls

    def extract_text_from_news(self):
        self._complete_news_info = {}
        self._paragraph_xpath = '/html/body/div[1]/section/p[{number}]'

        for each_news_url in self.news_urls:
            self._logger.info(
                'Extract data from {url}'.format(url=each_news_url))

            self._driver.get(each_news_url)
            exception_thrown = False
            paragraph_index = 1
            paragraphs = []
            while not exception_thrown:
                try:
                    self._wait_until_page_loads(
                        self._paragraph_xpath.format(number=paragraph_index),
                        self.PARAGRAPH_TIMEOUT
                    )

                    paragraphs.append(self._driver.find_element_by_xpath(
                        self._paragraph_xpath.format(
                            number=paragraph_index)).text)

                    paragraph_index += 1

                except TimeoutException:
                    exception_thrown = True

            self._complete_news_info[each_news_url] = ' '.join(paragraphs)

        # Write self._complete_news_info to a file, with current date.
        with open('complete_news_of_{name}_from_{day}_{month}_{year}'
                  '.json'.format(
                      name=self.NAME,
                      day=self._day,
                      month=self._month,
                      year=self._year), 'w') as f:
            f.write(dumps(self._complete_news_info))
            f.close()

        return self._complete_news_info

    def __del__(self):
        self._logger.info('Closing browser.')
        self._driver.quit()
